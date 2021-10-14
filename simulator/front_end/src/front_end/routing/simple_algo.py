from simulator.front_end.src.front_end.api import Frontend


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
