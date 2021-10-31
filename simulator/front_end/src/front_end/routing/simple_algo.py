from front_end.region_creation.fixed_region import Region


def simple_routing(region: Region, num_domains: int) -> int:
    # takes extra cpu/memory to compute hash, might have less dedup with small changes between regions
    return int.from_bytes(region.hash.digest()[:7], "little") % num_domains
    # with second algo you could stream directly to the destination domain rather than buffering all in the front_end
    # not necessary to implement for this simulator
#   return int.from_bytes(region.fingerprints[0][:7], "little") % num_domains
    # could look at first k fingerprints take min value fingerprint or max value
