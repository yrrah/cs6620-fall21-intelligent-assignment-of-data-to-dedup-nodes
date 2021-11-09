import os

from front_end.grpc.client import sendToBackend
from front_end.hash_files.get_hash_files import download_files
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
        self.REGION_FORMATION = os.environ['REGION_ALGO']
        
        # Used by the fixed algo
        self.REGION_SIZE = os.getenv('REGION_SIZE')
        if self.REGION_FORMATION == 'FIXED-SIZE':
            if self.REGION_SIZE is None:
                raise ValueError(
                    f'Environment variable for content-based region formation missing: '
                    f'REGION_SIZE:{self.REGION_SIZE} ')
            else:
                self.REGION_SIZE = int(self.REGION_SIZE)
        
        # The 3 below are used by the content-based-algo
        self.MIN_REGION_SIZE = os.getenv('MIN_REGION_SIZE')
        self.MAX_REGION_SIZE = os.getenv('MAX_REGION_SIZE')
        self.BIT_MASK = os.getenv('BIT_MASK')
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
        self.INPUT_DIR = os.getenv('INPUT_DIR')
        if self.INPUT_DIR is None:
            self.INPUT_DIR = '/var/input/'
        self.TRACES_WEBDIR = os.getenv('TRACES_WEBDIR')
        if self.TRACES_WEBDIR is None:
            self.TRACES_WEBDIR = 'https://tracer.filesystems.org/traces/'
        self.TRACES_SUBDIR = os.environ['TRACES_SUBDIR']
        self.TRACES_LIST = os.environ['TRACES_LIST']
        self.trace_file_names = []
        self.working_dir = self.INPUT_DIR+self.TRACES_SUBDIR

        # *****************************************
        self.ROUTING = os.environ['ROUTING']
        # DOMAINS specify the number of domains per pod
        self.DOMAINS = int(os.environ['DOMAINS'])
        # domains_to_pod maps a domain id to the pod.
        self.domains_to_pod = dict()
        self.back_end_ips = os.environ['BACKEND_IPS'].split(',')
        # Assign the domain ids to specific ip addresses -> each of them represent a service.
        self.assign_domains_to_pods()

    def assign_domains_to_pods(self) -> None:
        # The domain ids start from number 0
        domain_num = 0
        for ip in self.back_end_ips:
            for _ in range(0, self.DOMAINS):
                self.domains_to_pod[domain_num] = ip
                domain_num += 1

    def get_files(self):
        """
        open a file stream to the path / pod location on Openshift
        """
        with open(self.TRACES_LIST) as f:
            self.trace_file_names = f.read().splitlines()

        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)

        existing_files = set(next(os.walk(self.working_dir), (None, None, []))[2])

        to_be_downloaded = list(set(self.trace_file_names) - existing_files)

        download_files(self.working_dir, self.TRACES_WEBDIR+self.TRACES_SUBDIR, to_be_downloaded)

    def send_regions(self):
        for file_name in self.trace_file_names:
            hash_file = HashFile(self.working_dir + file_name)
            regions = region_factory(self.REGION_FORMATION, hash_file, self.REGION_SIZE, self.MAX_REGION_SIZE,
                                     self.MIN_REGION_SIZE, self.BIT_MASK)

            # Calculate the number of domains we have and pass it to the assignment code.
            number_domains = self.DOMAINS * len(self.back_end_ips)

            for region in regions:
                domain_to_send_to = simple_routing(region, number_domains)
                # This sends the region to the appropriate domain id
                sendToBackend(domain_to_send_to, self.domains_to_pod[domain_to_send_to] + ':50051', region)

    def shut_down(self):
        """
        kill back_end pods
        save / process results
        """
        pass

    def simulate(self):
        self.get_files()
        self.send_regions()
        self.shut_down()


if __name__ == '__main__':
    simulate = Simulator()
    simulate.send_regions()
