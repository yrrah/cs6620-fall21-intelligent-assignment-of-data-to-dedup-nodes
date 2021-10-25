from simulator.front_end.src.front_end.region_creation.fixed_region import Region


class KeyValueMap:
    """
    A map representation of a store that handles key, value pairs. Key --> domain_id and value
    the regions within it
    """

    def __init__(self, number_of_domains):
        """
        Predefine the number of domains to add
        """
        self.fingerprints = dict()
        self.current_total_mib = 0

        # Initialize the initial list with the set number of domains.
        for i in range(1, number_of_domains + 1):
            self.fingerprints[i] = set()

    def add_region(self, region: Region, domainId: int):
        """
        Add a region to the KV store and de-dup the fingerprints inside.
        :param region: The region being added to the map
        :param domainId : The domainId within the pod where the region needs to be added.
        :return: Tuple(int, int): bytes not de-duped, count of fingerprints not de-duped
        """
        region_fingerprints = set(region.fingerprints)
        non_duplicates = region_fingerprints - self.fingerprints[domainId]
        self.fingerprints[domainId].update(non_duplicates)
        non_duplicates_size = sum([len(x) for x in non_duplicates])
        self.current_total_mib += non_duplicates_size
        return non_duplicates_size, len(non_duplicates)

    def get_current_size(self):
        """

        :return: Total size of fingerprints in the kv store
        """
        return self.current_total_mib

    def get_current_count(self, domainId: int):
        """

        :return: Number of fingerprints in a domain of a kv store
        """
        return len(self.fingerprints[domainId])
