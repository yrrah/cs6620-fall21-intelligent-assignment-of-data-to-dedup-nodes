from typing import Callable, Tuple

from front_end.grpc.assignService_pb2 import Acknowledgement
from front_end.region_creation.region import Region
from front_end.routing.q_learning import QLearning
from front_end.routing.stateless import full_hash_7, first_fingerprint_7, min_fingerprint, max_fingerprint


def get_routing(function_name: str, q_learning: str or None, domains_per_pod: int,
                num_pods: int) -> Tuple[Callable[[Region, int], int],
                                        Callable[[Region, Acknowledgement], None] or None]:
    """
    @param function_name: name of the desired routing algorithm
    @param q_learning: True/False string -- modify the routing with Q_learning?
    @param domains_per_pod:
    @param num_pods:
    @return: Returns a tuple of (routing function, learning function)
    """
    routing_function = None
    if function_name == "FULL_HASH_7":
        routing_function = full_hash_7
    if function_name == "FIRST_FINGERPRINT_7" or function_name == "Q_LEARNING":
        routing_function = first_fingerprint_7
    if function_name == "MIN_FINGERPRINT":
        routing_function = min_fingerprint
    if function_name == "MAX_FINGERPRINT":
        routing_function = max_fingerprint
    if routing_function is None:
        raise ValueError(f"Invalid routing algorithm specified: {function_name}")

    if q_learning == "True" or function_name == "Q_LEARNING":
        q = QLearning(routing_function, domains_per_pod, num_pods)
        return q.route, q.learn
    else:
        return routing_function, None
