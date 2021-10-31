import fixed_region
from front_end.region_creation.content_defined_region_creation import create_content_defined_regions
from front_end.region_creation.input_streams import HashFile

"""
 This file contains the interface to create the region based on the different
 region creation algorithms.
"""


def get_hash_file(file_name: str) -> HashFile:
    hash_file = HashFile(file_name)
    return hash_file


def create_regions(algorithms: str, hash_file: HashFile):
    """
    :param algorithms: the type of the algorithm to create the region
    :param hash_file: the hash file object
    """
    if algorithms == "FIXED-SIZE":
        return fixed_region.create_fixed_regions(hash_file, 4)
    if algorithms == "CONTENT-DEFINED":
        return create_content_defined_regions(2, 8, 5, hash_file)
    else:
        raise ValueError("Region is too full to accept fingerprint")


def main():
    file_name = input("Enter file name with path: ")

    for region in create_regions("CONTENT-DEFINED", get_hash_file(file_name)):
        print(region.current_size, len(region.fingerprints))


if __name__ == "__main__":
    main()
