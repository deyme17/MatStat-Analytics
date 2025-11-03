from typing import List, Optional
from models.stat_distributions import registered_distributions, StatisticalDistribution

class DistributionRegister:
    """
    Wrapper for registered distributions with safe access.
    """
    def __init__(self):
        self._distributions = registered_distributions

    @property
    def distributions(self) -> List[str]:
        """Return list of available distribution names."""
        return list(self._distributions.keys())

    def get_dist(self, dist_name: str) -> Optional[type[StatisticalDistribution]]:
        """Return distribution class by name, or None if not found."""
        return self._distributions.get(dist_name)