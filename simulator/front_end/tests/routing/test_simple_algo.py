import unittest

from front_end.region_creation.fixed_region import create_fixed_regions
from front_end.region_creation.input_streams import HashFile
from front_end.routing.simple_algo import simple_routing


class TestSimpleAlgo(unittest.TestCase):
    """Tests for simple_algo"""

    def test_simple_algo(self):
        hash_file = HashFile("fslhomes-user006-2011-09-10.8kb.hash.anon")

        for region in create_fixed_regions(hash_file, 1):
            print(simple_routing(region, 10))
