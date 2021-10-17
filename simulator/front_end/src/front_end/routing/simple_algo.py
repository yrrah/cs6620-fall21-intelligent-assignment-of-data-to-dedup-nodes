from simulator.front_end.src.front_end.region_creation.fixed_region import create_fixed_regions, Region
from simulator.front_end.src.front_end.region_creation.input_streams import HashFile


def simple_routing(region: Region, num_domains: int) -> int:
    return int.from_bytes(region.hash.digest()[:7], "little") % num_domains


def main():
    hash_file = HashFile("fslhomes-user006-2011-09-10.8kb.hash.anon")

    for region in create_fixed_regions(hash_file, 1):
        print(simple_routing(region))


if __name__ == "__main__":
    main()

