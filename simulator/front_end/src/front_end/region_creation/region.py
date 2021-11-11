import hashlib

from front_end.grpc import assignService_pb2

'''
 This class represents a Region which contains the size of the region and 
 finger prints contained in it.
'''


class Region:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.current_size = 0
        self.fingerprints = []
        self.hash = hashlib.sha1()

    def add_fingerprint(self, fingerprint: bytes, chunk_size: int):
        if chunk_size + self.current_size <= self.max_size:
            self.fingerprints.append(assignService_pb2.Fingerprint(fingerPrint=fingerprint, fingerPrintSize=chunk_size))
            self.hash.update(fingerprint)
            self.current_size += chunk_size
        else:
            raise BufferError(f"Region is too full to accept fingerprint. {self.current_size}/{self.max_size}")
