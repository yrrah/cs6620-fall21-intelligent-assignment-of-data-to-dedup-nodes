import os
import tarfile

from grpc._channel import _InactiveRpcError
from timeit import default_timer as timer

from front_end.grpc.client import sendToBackend, kill_backend
from front_end.get_hash_files import download_files
from front_end.region_creation.input_streams import HashFile
from front_end.routing.simple_algo import simple_routing
from front_end.region_creation.create_region import region_factory


class Simulator:
    """
    Simulator represents the main entry point for the frontend code. All config file data are pulled up from the
    environment variables set in our deployment config in openshift.
    """

    def __init__(self):
        """
        The constructor fetches all the required info from the config files.
        """
        # Region Formation Config
        # ****************************************
        self.REGION_FORMATION = os.environ['SIMULATOR_REGION_ALGO']

        # Used by the fixed algo
        self.REGION_SIZE = os.getenv('SIMULATOR_REGION_SIZE')
        if self.REGION_FORMATION == 'FIXED-SIZE':
            if self.REGION_SIZE is None:
                raise ValueError(
                    f'Environment variable for content-based region formation missing: '
                    f'REGION_SIZE:{self.REGION_SIZE} ')
            else:
                self.REGION_SIZE = int(self.REGION_SIZE)

        # The 3 below are used by the content-based-algo
        self.MIN_REGION_SIZE = os.getenv('SIMULATOR_MIN_REGION_SIZE')
        self.MAX_REGION_SIZE = os.getenv('SIMULATOR_MAX_REGION_SIZE')
        self.BIT_MASK = os.getenv('SIMULATOR_BIT_MASK')
        if self.REGION_FORMATION == 'CONTENT-DEFINED':
            if self.MIN_REGION_SIZE is None or self.MAX_REGION_SIZE is None or self.BIT_MASK is None:
                raise ValueError(
                    f'Environment variable for content-based region formation missing: '
                    f'MIN_REGION_SIZE:{self.MIN_REGION_SIZE} '
                    f'MAX_REGION_SIZE:{self.MAX_REGION_SIZE} '
                    f'BIT_MASK:{self.BIT_MASK}')
            else:
                self.MIN_REGION_SIZE = int(self.MIN_REGION_SIZE)
                self.MAX_REGION_SIZE = int(self.MAX_REGION_SIZE)

        # Trace File Location Config
        # *****************************************
        self.INPUT_DIR = os.getenv('SIMULATOR_INPUT_DIR')
        if self.INPUT_DIR is None:
            self.INPUT_DIR = '/var/input/'
        self.OUTPUT_DIR = os.getenv('SIMULATOR_OUTPUT_DIR')
        if self.OUTPUT_DIR is None:
            self.OUTPUT_DIR = '/var/output/'
        self.log_file = None
        self.log_file_header = "domain, region bytes, non-dupe bytes, region fp count," \
                               " non-dupe fp count, route time, response time, user, hash date\n"
        self.TRACES_WEBDIR = os.getenv('SIMULATOR_TRACES_WEBDIR')
        if self.TRACES_WEBDIR is None:
            self.TRACES_WEBDIR = 'https://tracer.filesystems.org/traces/'
        self.TRACES_LISTS_DIR = os.getenv('SIMULATOR_TRACES_LISTS_DIR')
        if self.TRACES_LISTS_DIR is None:
            self.TRACES_LISTS_DIR = '/opt/app-root/src/src/traces/'
        self.TRACES_LISTS = os.environ['SIMULATOR_TRACES_LISTS'].split(',')
        self.trace_file_paths = []

        # *****************************************
        self.ROUTING = os.environ['SIMULATOR_ROUTING']
        # DOMAINS specify the number of domains per pod
        self.DOMAINS = int(os.environ['SIMULATOR_DOMAINS'])
        # domains_to_pod maps a domain id to the pod.
        self.domains_to_pod = dict()
        self.back_end_ips = os.environ['SIMULATOR_BACKEND_IPS'].split(',')
        # Assign the domain ids to specific ip addresses -> each of them represent a service.
        self.assign_domains_to_pods()
        self.setup_log()

    def assign_domains_to_pods(self) -> None:
        # The domain ids start from number 0
        domain_num = 0
        for ip in self.back_end_ips:
            for _ in range(0, self.DOMAINS):
                self.domains_to_pod[domain_num] = ip
                domain_num += 1

    def setup_log(self):
        if not os.path.exists(self.OUTPUT_DIR):
            os.makedirs(self.OUTPUT_DIR)

        self.log_file = open(self.OUTPUT_DIR + str(int(timer())) + '.csv', 'w')
        commas = ',' * 9
        self.log_file.writelines([f'{commas}{k}:{v}\n' for k, v in os.environ.items() if k.startswith('SIMULATOR_')])

        self.log_file.write(self.log_file_header)

    def get_files(self):
        """
        open a file stream to the path / pod location on Openshift
        """
        for list_name in self.TRACES_LISTS:
            sub_dir = list_name[:(list_name.rindex('_') + 1)].replace('_', '/')
            working_dir = self.INPUT_DIR + sub_dir

            with open(self.TRACES_LISTS_DIR + list_name) as f:
                trace_file_names = f.read().splitlines()

            if not os.path.exists(working_dir):
                os.makedirs(working_dir)

            existing_files = set(next(os.walk(working_dir), (None, None, []))[2])

            to_be_downloaded = list(set(trace_file_names) - existing_files)

            if len(to_be_downloaded) > 0:
                download_files(working_dir, self.TRACES_WEBDIR + sub_dir, to_be_downloaded)

            for trace_file_name in trace_file_names:
                self.trace_file_paths.append(working_dir + trace_file_name)

    def send_hash_file(self, file_path: str):
        print_freq = 10000
        print_count = print_freq
        print_header = True

        u = file_path.index('user')
        user_num = file_path[u + 4:u + 7]
        hash_date = file_path[u + 8:u + 18]
        try:
            hash_file = HashFile(file_path)
        except ValueError as e:
            print(e)
            return

        regions = region_factory(self.REGION_FORMATION, hash_file, self.REGION_SIZE, self.MAX_REGION_SIZE,
                                 self.MIN_REGION_SIZE, self.BIT_MASK)

        # Calculate the number of domains we have and pass it to the assignment code.
        number_domains = self.DOMAINS * len(self.back_end_ips)

        for region in regions:
            before_routing = timer()
            domain_to_send_to = simple_routing(region, number_domains)
            after_routing = timer()
            # This sends the region to the appropriate domain id
            response = sendToBackend(domain_to_send_to, self.domains_to_pod[domain_to_send_to] + ':50051', region)
            after_response = timer()
            log_line = f'{domain_to_send_to},{region.current_size},{response.nonDuplicatesSize},' \
                       f'{len(region.fingerprints)},{response.nonDuplicatesLength},' \
                       f'{after_routing - before_routing:.2E},{after_response - after_routing:.2E},' \
                       f'{user_num},{hash_date}\n'
            self.log_file.write(log_line)

            if print_count == 0:
                if print_header:
                    print(self.log_file_header)
                    print_header = False
                print(log_line, end='')
                print_count = print_freq
            else:
                print_count -= 1

    def send_trace_files(self):

        for file_path in self.trace_file_paths:
            print(file_path)
            suffix = '.8kb.hash.anon'

            # extract hash file from archive
            tar = tarfile.open(file_path, "r:bz2")
            hash_files = [m for m in tar.getmembers() if m.name.endswith(suffix)]
            for file in hash_files:
                # get just the file without directory structure
                file.name = os.path.basename(file.name)
            tar.extractall(path='.', members=hash_files)
            tar.close()
            if len(hash_files) > 0:
                self.send_hash_file('./' + hash_files[0].name)

                # remove the local copy of hash file
                os.remove('./' + hash_files[0].name)
            else:
                print(f'cant find hash file ending in {suffix}')

    def shut_down(self):
        """
        kill back_end pods
        save / process results
        """
        for backend in self.back_end_ips:
            try:
                kill_backend(backend + ':50051')
                print(f"{backend} shut down")
            except _InactiveRpcError as err:
                print("_InactiveRpcError: {0}".format(err))

    def simulate(self):
        self.get_files()
        self.send_trace_files()
        self.shut_down()


if __name__ == '__main__':
    sim = Simulator()
    sim.simulate()
