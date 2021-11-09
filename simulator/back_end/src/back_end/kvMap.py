# Made changes to work with rocksdb rather than the traditional python collections.
from collections import defaultdict

import pyrocksdb


def db_test():
    """
    example rocksdb usage
    @return:
    """
    db = pyrocksdb.DB()
    opts = pyrocksdb.Options()
    # for multi-thread
    # opts.IncreaseParallelism()
    # opts.OptimizeLevelStyleCompaction()
    opts.create_if_missing = True
    s = db.open(opts, 'db_files')
    print(s.code())
    assert (s.ok())
    # put
    opts = pyrocksdb.WriteOptions()
    s = db.put(opts, b"key1", b"value1")
    assert (s.ok())
    # get
    opts = pyrocksdb.ReadOptions()
    blob = db.get(opts, b"key1")
    print(blob.data)  # b"value1"
    print(blob.status.ok())  # true
    # delete
    opts = pyrocksdb.WriteOptions()
    s = db.delete(opts, b"key1")
    assert (s.ok())
    db.close()


class KeyValueMap:
    """
    A map representation of a store that handles key, value pairs.
    Key (domain_id + fingerprint) --> Value (empty)

    TODO: query rocksdb by key prefix (domain_id)?
        https://pyrocksdb.readthedocs.io/en/v0.4/api/interfaces.html#rocksdb.interfaces.SliceTransform
    """

    def __init__(self):
        """
        Predefine the number of domains to add
        """
        self.write_opts = pyrocksdb.WriteOptions()
        self.read_opts = pyrocksdb.ReadOptions()
        self.db = pyrocksdb.DB()
        opts = pyrocksdb.Options()
        # for multi-thread
        # opts.IncreaseParallelism()
        # opts.OptimizeLevelStyleCompaction()
        opts.create_if_missing = True
        s = self.db.open(opts, 'db_files')
        assert (s.ok())
        self.current_total_mib = 0
        self.domain_counts = defaultdict(int)

    def _set_key(self, domain_id: int, fingerprint: bytes):
        domain_bytes = domain_id.to_bytes(2, 'big')
        key = domain_bytes + fingerprint
        s = self.db.put(self.write_opts, key, domain_bytes)
        assert (s.ok())

    def _check_key(self, domain_id: int, fingerprint: bytes):
        key = domain_id.to_bytes(2, 'big') + fingerprint
        found = self.db.get(self.read_opts, key)
        return found.status.ok()

    # Just store fingerPrints based on domainId
    def add_region(self, region_sent_fingerprints, domain_id: int):
        """
        Add a region to the KV store and de-dup the fingerprints inside.
        :param region_sent_fingerprints: The fingerprints to be added to the map based on the domain id.
        :param domain_id : The domainId within the pod where the region needs to be added.
        :return: Tuple(int, int): bytes not de-duped, count of fingerprints not de-duped
        """
        non_duplicates = set()

        # looping as the GRPC sends a repeated array and we only store the fingerprints.
        for finger_print in region_sent_fingerprints:
            fp = finger_print.fingerPrint
            if not self._check_key(domain_id, fp):
                non_duplicates.add(fp)
                self._set_key(domain_id, fp)
                self.domain_counts[domain_id] += 1

        non_duplicates_size = sum([len(x) for x in non_duplicates])
        self.current_total_mib += non_duplicates_size
        return non_duplicates_size, len(non_duplicates)

    def get_current_size(self):
        """

        :return: Total size of fingerprints in the kv store
        """
        return self.current_total_mib

    def get_current_count(self, domain_id: int):
        """

        :return: Number of fingerprints stored in a particular domain in the KV store.
        """
        return  self.domain_counts[domain_id]
