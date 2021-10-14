from typing import Tuple


class BackendDomain:
    def __init__(self) -> None:
        """Backend Domain class


        Args:

        """

    def reset(self) -> None:
        """Initialize KV store, etc


        """

    def check_duplicate(self) -> Tuple[float, float]:
        """Deduplicate a given region and report performance

        Returns:
            optimal (Tuple[float, int]): (float) deduplication percentage
            and (float) load percentage

        """
        raise NotImplementedError


class BackendPod:
    def __init__(self) -> None:
        """Backend Pod class


        Args:

        """

    def reset(self, domains: int) -> None:
        """initialize given number of domains


        """

    def status(self) -> None:
        """Some kind of summary of the domains

        """
        raise NotImplementedError

    def send_region(self) -> None:
        """Send a region to a specified domain

        """
        raise NotImplementedError
