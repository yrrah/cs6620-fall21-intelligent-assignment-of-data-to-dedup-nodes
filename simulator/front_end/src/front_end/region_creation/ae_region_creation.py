from typing import Generator, Any

from front_end.grpc.assignService_pb2 import Region
from front_end.region_creation.input_streams import HashFile


def create_ae_regions(max_region_size: int, hash_file: HashFile) -> \
        Generator[Region, Any, None]:
    """
    Algorithm to create region based on MAXP which is max position reached till now.
    Such as whatever the maximum chunk size seen till now defines the boundary.
    :param max_region_size: Maximum region size in MiB
    :param hash_file: A hash file object that can be read to extract hashes.
    :return: the region objects
    """

    max_region_size = max_region_size * 1024 * 1024
    w = max_region_size / 2
    currentSize = 0
    region = Region(max_region_size)
    maxValue = 0
    while hash_file.num_files_processed < hash_file.total_files:
        hash_file.hashfile_next_file()
        while hash_file.num_hashes_processed_current_file < hash_file.current_file_total_chunks:
            fingerprint, compression, current_chunk_size = hash_file.hashfile_next_chunk()
            if current_chunk_size <= maxValue:
                if currentSize >= maxValue + current_chunk_size:
                    yield region
                    region = Region(max_region_size)
                    currentSize = current_chunk_size
                    region.add_fingerprint(fingerprint, current_chunk_size)
                    continue;
            else:
                maxValue = current_chunk_size

            region.add_fingerprint(fingerprint, current_chunk_size)
            currentSize += current_chunk_size
    yield region


def main():
    file_name = "/Volumes/Important/Fall-2021/CS6620/macos-2011-06-23-001346 2/macos-2011-06-23-001346.8kb.hash.anon"

    hash_file = HashFile(file_name)
    for region in create_ae_regions(4, hash_file):
        # sendToBackend(1, server_ip, region)
        print(region.current_size)


if __name__ == "__main__":
    main()
