from __future__ import print_function

import grpc
import assignService_pb2
import assignService_pb2_grpc
from simulator.front_end.src.front_end.region_creation.content_defined_region_creation import \
    create_content_defined_regions
from simulator.front_end.src.front_end.region_creation.fixed_region import create_fixed_regions
from simulator.front_end.src.front_end.region_creation.input_streams import HashFile

from simulator.front_end.src.front_end.region_creation.region import Region
import simulator.front_end.src.front_end.region_creation.content_defined_region_creation

def sendToBackend(domainID, region):
    """
    A client code that sends a region to the backend server,based on domainId.
    """
    channel = grpc.insecure_channel('localhost:50051')
    stub = assignService_pb2_grpc.RegionReceiveServiceStub(channel)
    fingerprints_to_add = assignService_pb2.Fingerprint()
    for i in range(0, len(region.fingerprints)):
        temp = fingerprints_to_add.fingerPrint.add()
        temp.fingerPrint = region.fingerprints[i]

    # Assigning to the region class
    region_to_send = assignService_pb2.Region(domainNumber=domainID, maxSize=region.max_size,
                                              currentSize=region.current_size,
                                              fingerPrint=fingerprints_to_add)
    # Get the response from the server(like a callback)
    response = stub.AssignRegion(region_to_send)
    print("response from the backend service")
    return response

# TODO : Integrate with the assignment service

if __name__ == '__main__':

    hash_file = HashFile("C:/Users/nikhi/Documents/Cloud Computing/Dedup "
                         "domains/cs6620-fall21-intelligent-assignment-of-data-to-dedup-nodes"
                         "/simulator/hash_files/fslhomes-user006-2011-09-22.8kb.hash.anon")

    for region in create_fixed_regions(hash_file, 1):
        sendToBackend(1, region)