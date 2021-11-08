from __future__ import print_function

import os

import grpc

from front_end.grpc import assignService_pb2_grpc, assignService_pb2
from front_end.region_creation.fixed_region import create_fixed_regions
from front_end.region_creation.input_streams import HashFile


def sendToBackend(domain: int, back_end_address: str, region):
    """
    A client code that sends a region to the backend server,based on domainId.
    """
    with grpc.insecure_channel(back_end_address) as channel:
        stub = assignService_pb2_grpc.RegionReceiveServiceStub(channel)
        region_to_send = assignService_pb2.Region()
        for i in range(0, len(region.fingerprints)):
            region_to_send.fingerPrint.append(assignService_pb2.Fingerprint(fingerPrint=region.fingerprints[i]))

        region_to_send.domainNumber = domain
        region_to_send.maxSize = region.max_size
        region_to_send.currentSize = region.current_size
        # Assigning to the region class

        # Get the response from the server(like a callback)
        response = stub.AssignRegion(region_to_send)
        print("response from the backend service -> nonDuplicatesSize = {} and nonDuplicatesLength = {}".
              format(response.nonDuplicatesSize, response.nonDuplicatesLength))
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

