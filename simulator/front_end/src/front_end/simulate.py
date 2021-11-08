import os
from create_region import region_factory
from simple_algo import simple_routing
from client import sendToBackend

class Simulator:
    """
    Simulator represents the main entry point for the frontend code. All config file data are pulled up from the
    environment variables set in our deployment config in openshift.
    """

    def __init__(self):
        """
        The constructor fetches all the required info from the config files.
        """
        # Region Formation configs to be set.
        # ****************************************
        self.REGION_FORMATION = os.environ['REGION_ALGO']
        self.REGION_SIZE = os.environ['REGION_SIZE'] # Used by the fixed algo
        # The 3 below are used by the content-based-algo
        self.MIN_REGION_SIZE = os.environ['MIN_REGION_SIZE']
        self.MAX_REGION_SIZE = os.environ['MAX_REGION_SIZE']
        self.BIT_MASK = os.environ['BIT_MASK']
        # *****************************************
        self.ROUTING = os.environ['ROUTING']
        # DOMAINS specify the number of domains per pod
        self.DOMAINS = os.environ['DOMAINS']
        # domains_to_pod maps a domain id to the pod.
        self.domains_to_pod = dict()
        self.back_end_ips = os.environ['BACKEND_IPS'].split(',')
        # Assign the domain ids to specific ip addresses -> each of them represent a service.
        self.assign_domains_to_pods()

    def assign_domains_to_pods(self) -> None:
        # The domain ids start from number 1
        num = 1
        for ip in self.back_end_ips:
            for i in range(0, self.DOMAINS):
                self.domains_to_pod[num] = ip
                num += 1

    def get_variables(self):
        """
        use environment variables to configure the simulator
        """
        pass
        # REGION_FORMATION = FIXED
        # REGION_SIZE = 4
        # ROUTING = SIMPLE
        # SIMULATOR_MODE = RUN
        # back_end_ips = os.environ['BACKEND_IPS'].split(',')

    def get_files(self):
        """
        open a file stream to the path / pod location on Openshift
        """
        pass

    def send_regions(self):
        file = get_files()
        regions = region_factory(self.REGION_FORMATION, file, self.REGION_SIZE, self.MAX_REGION_SIZE,
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

    def simulate(self):
        get_variables()
        get_files()
        send_regions()
        shut_down()


if __name__ == '__main__':
    simulate = Simulator()
    simulate.send_regions()
