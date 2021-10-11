from abc import ABC, abstractmethod


class Frontend(ABC):
    def __init__(self) -> None:
        """Abstract class

        Implements common functions

        Args:

        """
        raise NotImplementedError

    def reset(self) -> None:
        """Initialize or reset values
        """
        raise NotImplementedError

    def get_input_stream(self) -> None:
        """Initialize or reset values

        Args:

        """
        raise NotImplementedError

    @abstractmethod
    def create_regions(self):
        """
        given an input stream of fingerprints, yield regions

        Args:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def route_region(self) -> None:
        """
        given the state of the cluster, return index of a domain

        Args:

        """
        raise NotImplementedError


class SimpleAlgo(Frontend):
    def __init__(self) -> None:
        """Simulator with simple algorithms

        Args:

        """
        super().__init__()

    def create_regions(self):
        """
        given an input stream of fingerprints, yield regions

        Args:
        :return:
        """
        yield None

    def route_region(self) -> None:
        """

        Args:

        """
        raise NotImplementedError