from typing import Generator, Any

from simulator.front_end.src.front_end.region_creation.input_streams import HashFile
from simulator.front_end.src.front_end.region_creation.region import Region


def bytes_to_int(hex_string) -> int:
    """
    :param hex_string: a string formatted like 3f:8d:1a:35:a8:ff
    :return: integer value of the hex string
    """

    return int.from_bytes(hex_string, "big")


def create_content_defined_regions(min_region_size: int, max_region_size: int, mask: int, hash_file: HashFile) -> \
        Generator[Region, Any, None]:
    """
    :param min_region_size: Minimum region size in MiB
    :param max_region_size: Maximum region size in MiB
    :param mask: mask bits to mask the chunks
    :param hash_file: A hash file object that can be read to extract hashes.
    :return: the region objects
    """

    max_region_size = (max_region_size * 1024 * 1024)
    min_region_size = (min_region_size * 1024 * 1024)
    mask = (mask * 1024 * 1024)
    region = Region(max_region_size)

    while hash_file.num_files_processed < hash_file.total_files:
        hash_file.hashfile_next_file()
        while hash_file.num_hashes_processed_current_file < hash_file.current_file_total_chunks:
            fingerprint, compression, current_chunk_size = hash_file.hashfile_next_chunk()

            if region.current_size >= min_region_size:
                if (bytes_to_int(fingerprint) & mask) == mask:
                    yield region
                    region = Region(max_region_size)
                elif region.current_size + current_chunk_size > max_region_size:
                    yield region
                    region = Region(max_region_size)
            region.add_fingerprint(fingerprint, current_chunk_size)

    yield region

