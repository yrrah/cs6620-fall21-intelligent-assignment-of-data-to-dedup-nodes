import hashlib
from typing import Generator, Any

from simulator.front_end.src.front_end.region_creation.input_streams import HashFile


class Region:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.current_size = 0
        self.fingerprints = []
        self.hash = hashlib.sha1()

    def add_fingerprint(self, fingerprint: bytes):
        if len(fingerprint) + self.current_size <= self.max_size:
            self.fingerprints.append(fingerprint)
            self.hash.update(fingerprint)
            self.current_size += len(fingerprint)
        else:
            raise BufferError(f"Region is too full to accept fingerprint. {self.current_size}/{self.max_size}")


def create_fixed_regions(hash_file: HashFile, size_mib: int) -> Generator[Region, Any, None]:
    """

    :param size_mib: Fixed region size in MiB
    :param hash_file: A hash file object that can be read to extract hashes.
    :return:
    """
    max_region_size = (size_mib * 1024 * 1024)
    current_region = Region(max_region_size)

    while hash_file.num_files_processed < hash_file.total_files:
        hash_file.hashfile_next_file()
        while hash_file.num_hashes_processed_current_file < hash_file.current_file_total_chunks:
            fingerprint, compression = hash_file.hashfile_next_chunk()
            if len(fingerprint) + current_region.current_size > max_region_size:
                yield current_region
                current_region = Region(max_region_size)

            current_region.add_fingerprint(fingerprint)

    yield current_region


def main():
    hash_file = HashFile("fslhomes-user006-2011-09-10.8kb.hash.anon")

    for region in create_fixed_regions(hash_file, 1):
        print(region.current_size, len(region.fingerprints))


if __name__ == "__main__":
    main()


