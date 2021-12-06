from typing import Generator, Any

from front_end.region_creation.region import Region
from front_end.region_creation.input_streams import HashFile


def bytes_to_int(byte_string) -> int:
    """
    :param byte_string: a string formatted like b'\xd4\x053K\xd8\xea'
    :return: integer value of the byte stream
    """

    return int.from_bytes(byte_string, "big")


def create_tttd_regions(minT: int, maxT: int, secondD: int, mainD: int, hash_file: HashFile) -> \
    Generator[Region, Any, None]:
    """
        minT: minimum threshold (around 1 to 2 MB)
        maxT: maximum threshold (around 4 to 5 MB)
        secondD: second divisor (270)
        mainD: main divisor (540)

    """

    minT = minT * 1024 * 1024
    maxT = maxT * 1024 * 1024
    secondD = secondD
    mainD = mainD

    # TTTD region creation
    currentP = 0
    backupBreak = 0
    region = Region(maxT)
    while hash_file.num_files_processed < hash_file.total_files:
        hash_file.hashfile_next_file()
        while hash_file.num_hashes_processed_current_file < hash_file.current_file_total_chunks:
            fingerprint, compression, current_chunk_size = hash_file.hashfile_next_chunk()
            print(fingerprint)
            if currentP < minT:
                region.add_fingerprint(fingerprint, current_chunk_size)
                currentP += current_chunk_size
                continue
            if (bytes_to_int(fingerprint) % secondD) == secondD - 1: backupBreak = currentP
            if (bytes_to_int(fingerprint) % mainD) == mainD - 1:
                yield region
                backupBreak = 0
                currentP = 0
                region = Region(maxT)
                region.add_fingerprint(fingerprint, current_chunk_size)
                currentP += current_chunk_size
                continue
            if currentP + current_chunk_size < maxT:
                region.add_fingerprint(fingerprint, current_chunk_size)
                currentP += current_chunk_size
                continue
            if backupBreak != 0:
                yield region
                backupBreak = 0
                currentP = 0
                region = Region(maxT)
            elif currentP + current_chunk_size > maxT:
                yield region
                backupBreak = 0
                currentP = 0
                region = Region(maxT)
            region.add_fingerprint(fingerprint, current_chunk_size)
            currentP += current_chunk_size
    yield region


def main():
    file_name = "/Volumes/Important/Fall-2021/CS6620/macos-2011-06-23-001346 2/macos-2011-06-23-001346.8kb.hash.anon"

    hash_file = HashFile(file_name)
    for region in create_tttd_regions(2, 4, 270, 540, hash_file):
        # sendToBackend(1, server_ip, region)
        print(region.current_size)


if __name__ == "__main__":
    main()
