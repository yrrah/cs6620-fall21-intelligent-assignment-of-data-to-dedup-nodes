from __future__ import print_function

import grpc

from front_end.grpc import assignService_pb2_grpc, assignService_pb2
from front_end.grpc.assignService_pb2 import Acknowledgement
from front_end.region_creation.input_streams import HashFile
from simulator.front_end.src.front_end.region_creation.ae_region_creation import create_ae_regions


def kill_backend(back_end_address: str) -> None:
    with grpc.insecure_channel(back_end_address) as channel:
        stub = assignService_pb2_grpc.RegionReceiveServiceStub(channel)
        region_to_send = assignService_pb2.Region()
        region_to_send.domainNumber = -1
        stub.AssignRegion(region_to_send)


def sendToBackend(domain: int, back_end_address: str, region) -> Acknowledgement:
    """
    A client code that sends a region to the backend server,based on domainId.
    """
    with grpc.insecure_channel(back_end_address) as channel:
        stub = assignService_pb2_grpc.RegionReceiveServiceStub(channel)

        # Assigning to the region class
        region_to_send = assignService_pb2.Region()
        region_to_send.fingerPrint.extend(region.fingerprints)
        region_to_send.domainNumber = domain
        region_to_send.maxSize = region.max_size
        region_to_send.currentSize = region.current_size

        # Get the response from the server(like a callback)
        response = stub.AssignRegion(region_to_send)
    return response


def shutdown_backend(backend_address):
    """
    A client method that calls the ShutDownBackend method in the server to kill it.
    """
    channel = grpc.insecure_channel(backend_address)
    stub = assignService_pb2_grpc.RegionReceiveServiceStub(channel)
    print('Pod with address {0} has been shut down '.format(backend_address))
    stub.ShutDownPod(assignService_pb2.Empty())


def hash_file_demo(filename: str, ip_address):
    """
    Send the region to a backend server based on the ip_address sent to it by the simulate code-->
    which in turn gets it from the assignment code.
    """
    hash_file = HashFile(filename)
    server_ip = ip_address + ':50051'
    for region in create_ae_regions(4, hash_file):
        response = sendToBackend(1, server_ip, region)
        print(response)

    print('shutdown pod with {0}'.format(server_ip))
    shutdown_backend(ip_address + ':50051')


if __name__ == '__main__':
    hash_file_demo("../../traces/fslhomes-user006-2012-01-02.8kb.hash.anon", "localhost")
