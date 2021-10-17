from simulator.front_end.src.front_end.region_creation.fixed_region import Region


class KeyValueStore:
    def __init__(self):
        self.fingerprints = set()
        self.current_total_mib = 0

    def add_region(self, region: Region):
        """
        Add a region to the KV store and de-dup the fingerprints inside.
        :param region:
        :return: Tuple(int, int): bytes not de-duped, count of fingerprints not de-duped
        """
        region_fingerprints = set(region.fingerprints)
        non_duplicates = region_fingerprints - self.fingerprints
        self.fingerprints.update(non_duplicates)
        non_duplicates_size = sum([len(x) for x in non_duplicates])
        self.current_total_mib += non_duplicates_size
        return non_duplicates_size, len(non_duplicates)

    def get_current_size(self):
        """

        :return: Total size of fingerprints in the kv store
        """
        return self.current_total_mib

    def get_current_count(self):
        """

        :return: Number of fingerprints in kv store
        """
        return len(self.fingerprints)





