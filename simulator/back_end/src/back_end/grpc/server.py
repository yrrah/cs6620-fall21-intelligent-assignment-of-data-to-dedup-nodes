"""This class represents the server for the GRPC service. It receives a region from the frontend and it passes the
region to the domains (the backend service)
"""
from __future__ import print_function
from concurrent import futures
import logging
import grpc
import assignService_pb2
import assignService_pb2_grpc
from simulator.front_end.src.front_end.region_creation.region import Region
from simulator.back_end.src.back_end.kv_store.kvMap import KeyValueMap


class AssignToDomain(assignService_pb2_grpc.RegionReceiveServiceServicer):
    """
    This class is the server which is going to assign the regions to the backend of the domain.
    """

    # Here kv_store represents the domains and the fingerprints which we will store in the pod.
    kv_store = KeyValueMap(1)

    def AssignRegion(self, request, context):
        print("In the assign method")
        print(type(request.fingerPrint))
        non_duplicate_size, non_duplicates_length = self.kv_store.add_region(request.fingerPrint, 1)
        return assignService_pb2.Acknowledgement(nonDuplicatesSize=non_duplicate_size,
                                                 nonDuplicatesLength=non_duplicates_length)
    # TODO : Write some code for getting some stats from the domains.


def serve():
    """
    Method that starts a server and listens to a port for client calls
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    assignService_pb2_grpc.add_RegionReceiveServiceServicer_to_server(AssignToDomain(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
