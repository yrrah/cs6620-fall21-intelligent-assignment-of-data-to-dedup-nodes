#Made changes to work with rocksdb rather than the traditional python collections.

import rocksdb

class KeyValueMap:
    """
    A map representation of a store that handles key, value pairs. Key --> domain_id and value
    the regions within it.
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

    #Just store fingerPrints based on domainId
    def add_region(self, region_sent_fingerprints, domain_id: int):
        """
        Add a region to the KV store and de-dup the fingerprints inside.
        :param finger_print: The fingerprints to be added to the map based on the domain id.
        :param domain_id : The domainId within the pod where the region needs to be added.
        :return: Tuple(int, int): bytes not de-duped, count of fingerprints not de-duped
        """
        region_fingerprints = set()

        #looping as the GRPC sends a repeated array and we only store the fingerprints.
        for finger_print in region_sent_fingerprints:
            region_fingerprints.add(finger_print.fingerPrint)
        non_duplicates = region_fingerprints - self.fingerprints[domain_id]
        self.fingerprints[domain_id].update(non_duplicates)
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

        :return: Number of fingerprints stored in a particular domain in the KV store.
        """
        return len(self.fingerprints[domainId])
