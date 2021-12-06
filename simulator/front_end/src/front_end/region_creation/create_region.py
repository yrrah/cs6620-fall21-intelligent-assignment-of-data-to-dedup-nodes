from front_end.region_creation.fixed_region import create_fixed_regions
from front_end.region_creation.content_defined_region_creation import create_content_defined_regions
from front_end.region_creation.input_streams import HashFile
from front_end.region_creation.two_threshold_two_divisor_region_creation import create_tttd_regions
from front_end.region_creation.ae_region_creation import create_ae_regions

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
        return create_fixed_regions(hash_file, 4)
    if algorithms == "CONTENT-DEFINED":
        return create_content_defined_regions(2, 8, 5, hash_file)
    else:
        raise ValueError("Region is too full to accept fingerprint")


def region_factory(algorithm: str, hash_file: HashFile, region_size, min_size, max_size, bit_mask, main_d, second_d):
    if algorithm == "FIXED-SIZE":
        return create_fixed_regions(hash_file, region_size)

    if algorithm == "CONTENT-DEFINED":
        return create_content_defined_regions(min_size, max_size, bit_mask, hash_file)

    if algorithm == "TTTD":
        return create_tttd_regions(min_size, max_size, second_d, main_d, hash_file)

    if algorithm == "AE":
        return create_ae_regions(min_size, max_size, hash_file)

    else:
        raise ValueError("Please enter a correct region formation algorithm!")


def main():
    file_name = input("Enter file name with path: ")

    for region in create_regions("CONTENT-DEFINED", get_hash_file(file_name)):
        print(region.current_size, len(region.fingerprints))


if __name__ == "__main__":
    main()
