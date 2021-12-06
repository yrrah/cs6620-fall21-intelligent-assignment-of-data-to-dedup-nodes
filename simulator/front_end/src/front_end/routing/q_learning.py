from typing import Callable, Sequence, Dict

import numpy as np
from numpy import ndarray

from front_end.grpc.assignService_pb2 import Acknowledgement
from front_end.region_creation.region import Region


def argmax_random(arr: Sequence[float], rng: type(np.random.Generator)) -> int:
    """Argmax that breaks ties randomly
    Takes in a list of values and returns the index of the item with the highest value, breaking ties randomly.
    Args:
        :param arr: sequence of values
        :param rng: numpy random number generator for making choices
    """
    max_value = np.max(arr)
    max_indices = np.nonzero(np.isclose(arr, max_value))[0]
    if max_indices.size == 1:
        return max_indices[0]

    return rng.choice(max_indices)


def create_epsilon_policy(q_values: Dict[int, ndarray], epsilon: float) -> Callable:
    """Creates an epsilon soft policy from Q values.
    Args:
        @param epsilon: softness parameter
        @param q_values: current Q-values
    Returns:
        get_action (Callable): Takes a state as input and outputs an action
    """
    # Get number of actions
    num_actions = len(q_values[0])
    rng = np.random.default_rng()

    def get_action(state: int) -> int:
        # Take a random action with probability epsilon
        if epsilon > 0 and np.random.random() < epsilon:
            return rng.choice(range(0, num_actions))
        # break ties arbitrarily
        return argmax_random(q_values[state], rng)

    return get_action


def default_q_value(domains_per_pod: int, num_pods: int):
    q_values = {}
    for d in range(domains_per_pod * num_pods):
        best_pod = int(d / domains_per_pod)
        q_values[d] = np.zeros(num_pods)
        q_values[d][best_pod] = 1.0
    return q_values


class QLearning:

    def __init__(self, routing_function: Callable[[Region, int], int], domains_per_pod, num_pods,
                 gamma: float = 0.9, epsilon: float = 0.01, step_size: float = 0.5):
        self.routing_function = routing_function
        self.gamma = gamma
        self.epsilon = epsilon
        self.step_size = step_size
        self.state_space = domains_per_pod * num_pods
        self.action_space = num_pods
        self.domains_per_pod = domains_per_pod
        self.Q = default_q_value(self.domains_per_pod, self.action_space)
        self.policy = create_epsilon_policy(self.Q, epsilon)
        self.rng = np.random.default_rng()
        self.prev_state = 0
        self.prev_action = 0
        self.prev_reward = 0
        self.prev_reward_string = ''
        self.log_interval = 1000
        self.log_counter = self.log_interval

    def route(self, region: Region, number_domains: int):
        # use a stateless routing algo to limit state space to number of domains
        state = self.routing_function(region, number_domains)
        default_pod = int(state / self.domains_per_pod)
        policy_pod = self.policy(state)

        best_action = argmax_random(self.Q[state], self.rng)
        self.Q[self.prev_state][self.prev_action] += self.step_size * (
                self.prev_reward + (self.gamma * self.Q[state][best_action]) - self.Q[self.prev_state][
                self.prev_action])

        self.prev_state = state
        self.prev_action = policy_pod

        if self.log_counter == 0:
            domain = 0
            for p in range(self.action_space):
                row = np.zeros(self.action_space)
                for d in range(self.domains_per_pod):
                    row += self.Q[domain]
                    domain += 1
                print(f'pod {p}: {row}')
            # print(f'domain 364: {self.Q[364]}')
            print(self.prev_reward_string)
            self.log_counter = self.log_interval
        else:
            self.log_counter -= 1

        # use selected action to redirect region to a better pod
        return state + (policy_pod - default_pod) * self.domains_per_pod

    def learn(self, region: Region, ack: Acknowledgement):
        self.prev_reward = 1 - (ack.nonDuplicatesLength / len(region.fingerprints))
        self.prev_reward_string = f'prev_reward = {(1 - (ack.nonDuplicatesLength / len(region.fingerprints)))}'

        # self.prev_reward = (1 - (ack.nonDuplicatesLength / len(region.fingerprints))) * (1 - (ack.cpuPercent / 100))
        # self.prev_reward_string = f'prev_reward = {(1 - (ack.nonDuplicatesLength / len(region.fingerprints)))} ' \
        #                           f'* {(1 - (ack.cpuPercent / 100))}'
