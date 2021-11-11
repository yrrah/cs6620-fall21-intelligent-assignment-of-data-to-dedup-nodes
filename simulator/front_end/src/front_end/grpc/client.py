from __future__ import print_function

import grpc

from front_end.grpc import assignService_pb2_grpc, assignService_pb2
from front_end.grpc.assignService_pb2 import Acknowledgement
from front_end.region_creation.fixed_region import create_fixed_regions
from front_end.region_creation.input_streams import HashFile


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


def hash_file_demo(filename: str, ip_address):
    """
    Send the region to a backend server based on the ip_address sent to it by the simulate code-->
    which in turn gets it from the assignment code.
    """
    hash_file = HashFile(filename)
    server_ip = ip_address + ':50051'
    for region in create_fixed_regions(hash_file, 4):
        sendToBackend(1, server_ip, region)


if __name__ == '__main__':
    hash_file_demo("../hash_files/fslhomes-user006-2011-09-10.8kb.hash.anon")

