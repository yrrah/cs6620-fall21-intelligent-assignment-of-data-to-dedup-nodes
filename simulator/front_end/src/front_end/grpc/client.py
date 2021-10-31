from __future__ import print_function

import grpc

from front_end.grpc import assignService_pb2_grpc, assignService_pb2
from front_end.region_creation.fixed_region import create_fixed_regions
from front_end.region_creation.input_streams import HashFile


def sendToBackend(domainID, region):
    """
    A client code that sends a region to the backend server,based on domainId.
    """
    channel = grpc.insecure_channel('localhost:50051')
    stub = assignService_pb2_grpc.RegionReceiveServiceStub(channel)
    region_to_send = assignService_pb2.Region()
    for i in range(0, len(region.fingerprints)):
        region_to_send.fingerPrint.append(assignService_pb2.Fingerprint(fingerPrint=region.fingerprints[i]))

    region_to_send.domainNumber = domainID
    region_to_send.maxSize = region.max_size
    region_to_send.currentSize = region.current_size
    # Assigning to the region class

    # Get the response from the server(like a callback)
    response = stub.AssignRegion(region_to_send)
    print("response from the backend service -> nonDuplicatesSize = {} and nonDuplicatesLength = {}".
          format(response.nonDuplicatesSize, response.nonDuplicatesLength))
    return response


# TODO : Integrate with the assignment service

def hash_file_demo(filename: str):
    hash_file = HashFile(filename)
    for region in create_fixed_regions(hash_file, 4):
        sendToBackend(1, region)


if __name__ == '__main__':
    hash_file_demo("../hash_files/fslhomes-user006-2011-09-10.8kb.hash.anon")

