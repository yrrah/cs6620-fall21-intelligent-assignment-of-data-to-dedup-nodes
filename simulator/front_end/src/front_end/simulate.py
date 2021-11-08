import os


def get_variables():
    """
    use environment variables to configure the simulator
    """
    pass
    # REGION_FORMATION = FIXED
    # REGION_SIZE = 4
    # ROUTING = SIMPLE
    # SIMULATOR_MODE = RUN
    back_end_ips = os.environ['BACKEND_IPS'].split(',')


def get_files():
    """
    open a file stream to the path / pod location on Openshift
    """
    pass


def send_regions(back):
    # num_pods = len(back_end_ips)
    # hash_file = HashFile(filename)
    # server_ip = os.environ['SERVER_IP'] + ':50051'
    #     for region in create_fixed_regions(hash_file, 4):
    #     sendToBackend(1, server_ip, region)
    pass


def shut_down():
    """
    kill back_end pods
    save / process results
    """


def simulate():
    get_variables()
    get_files()
    send_regions()
    shut_down()
