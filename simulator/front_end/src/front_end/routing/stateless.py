import numpy as np

from front_end.region_creation.fixed_region import Region


def get_first_n_MB_fingerprints(n: int, region: Region):
    """

    @param n:
    @param region:
    @return:
    """
    search_range = (n * 1024 * 1024)
    fp_bytes = 0
    fp_hashes = []
    for fp in region.fingerprints:
        fp_bytes += fp.fingerPrintSize
        fp_hashes.append(int.from_bytes(fp.fingerPrint, "little"))
        if fp_bytes >= search_range:
            break
    return fp_hashes


def full_hash_7(region: Region, num_domains: int) -> int:
    # takes extra cpu/memory to compute hash, might have less dedup with small changes between regions
    return int.from_bytes(region.hash.digest()[:7], "little") % num_domains


def first_fingerprint_7(region: Region, num_domains: int) -> int:
    # with this algo you could stream directly to the destination domain rather than buffering all in the front_end
    # but that's not necessary to implement for this simulator
    return int.from_bytes(region.fingerprints[0].fingerPrint[:7], "little") % num_domains


def min_fingerprint(region: Region, num_domains: int) -> int:
    fp_hashes = get_first_n_MB_fingerprints(1, region)
    min_hash = np.min(np.array(fp_hashes))
    return min_hash % num_domains


def max_fingerprint(region: Region, num_domains: int) -> int:
    fp_hashes = get_first_n_MB_fingerprints(1, region)
    max_hash = np.max(np.array(fp_hashes))
    return max_hash % num_domains
