from typing import Generator, Any

from front_end.region_creation.input_streams import HashFile
from front_end.region_creation.region import Region

"""
    This file contains the the algorithm to create regions of fixed size.
"""


def create_fixed_regions(hash_file: HashFile, size_mib: int) -> Generator[Region, Any, None]:
    """

    :param size_mib: Fixed region size in MiB
    :param hash_file: A hash file object that can be read to extract hashes.
    :return:
    """
    max_region_size = (size_mib * 1024 * 1024)
    region = Region(max_region_size)

    while hash_file.num_files_processed < hash_file.total_files:
        hash_file.hashfile_next_file()
        while hash_file.num_hashes_processed_current_file < hash_file.current_file_total_chunks:
            fingerprint, compression, current_chunk_size = hash_file.hashfile_next_chunk()
            if current_chunk_size + region.current_size > max_region_size:
                yield region
                region = Region(max_region_size)

            region.add_fingerprint(fingerprint, current_chunk_size)

    yield region


def main():
    hash_file = HashFile("fslhomes-user006-2011-09-10.8kb.hash.anon")

    for region in create_fixed_regions(hash_file, 4):
        print(region.current_size, len(region.fingerprints))


if __name__ == "__main__":
    main()
