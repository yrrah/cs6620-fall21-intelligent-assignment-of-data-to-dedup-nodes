"""This class represents the server for the GRPC service. It receives a region from the frontend and it passes the
region to the domains (the backend service)
"""
from __future__ import print_function

import logging
import threading
import grpc
import psutil

from concurrent import futures
from back_end.grpc import assignService_pb2_grpc, assignService_pb2
from back_end.kv_store import RocksDBStore


class AssignToDomain(assignService_pb2_grpc.RegionReceiveServiceServicer):
    """
    This class is the server which is going to assign the regions to the backend of the domain.
    """
    def __init__(self, stop_event):
        self._stop_event = stop_event
        # Here kv_store represents the domains and the fingerprints which we will store in the pod.
        self.kv_store = RocksDBStore()
        self.region_count = 0

    def AssignRegion(self, request, context):
        self.region_count += 1
        if self.region_count % 100 == 0:
            print(self.kv_store.domain_counts)

        if request.domainNumber == -1:
            self._stop_event.set()
            return assignService_pb2.Acknowledgement(nonDuplicatesSize=-1, nonDuplicatesLength=-1)

        non_duplicate_size, non_duplicates_length = self.kv_store.add_region(request.fingerPrint, request.domainNumber)
        return assignService_pb2.Acknowledgement(nonDuplicatesSize=non_duplicate_size,
                                                 nonDuplicatesLength=non_duplicates_length,
                                                 cpuPercent=psutil.cpu_percent())
    # TODO : Write some code for getting some stats from the domains.


def serve():
    """
    Method that starts a server and listens to a port for client calls
    """
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    assignService_pb2_grpc.add_RegionReceiveServiceServicer_to_server(AssignToDomain(stop_event), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    stop_event.wait()
    server.stop(grace=None)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
