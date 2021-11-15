from typing import Callable

from front_end.region_creation.region import Region
from front_end.routing.simple import full_hash_7, first_fingerprint_7


def get_routing(function_name: str) -> Callable[[Region, int], int]:
    if function_name == "FULL_HASH_7":
        return full_hash_7
    if function_name == "FIRST_FINGERPRINT_7":
        return first_fingerprint_7

    raise ValueError(f"Invalid routing algorithm specified: {function_name}")

