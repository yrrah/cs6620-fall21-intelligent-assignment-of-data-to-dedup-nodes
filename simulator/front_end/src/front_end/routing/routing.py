from typing import Callable, Tuple

from front_end.grpc.assignService_pb2 import Acknowledgement
from front_end.region_creation.region import Region
from front_end.routing.q_learning import QLearning
from front_end.routing.simple import full_hash_7, first_fingerprint_7, first_fingerprint


def get_routing(function_name: str, domains_per_pod: int,
                num_pods: int) -> Tuple[Callable[[Region, int], int],
                                        Callable[[Region, Acknowledgement], None] or None]:
    """

    @param domains_per_pod:
    @param function_name:
    @param num_pods:
    @return: Returns a tuple of (routing function, learning function)
    """
    if function_name == "FULL_HASH_7":
        return full_hash_7, None
    if function_name == "FIRST_FINGERPRINT_7":
        return first_fingerprint_7, None
    if function_name == "FIRST_FINGERPRINT":
        return first_fingerprint, None
    if function_name == "Q_LEARNING":
        q = QLearning(domains_per_pod, num_pods)
        return q.route, q.learn
    raise ValueError(f"Invalid routing algorithm specified: {function_name}")
