from typing import List, Optional
from models.stat_distributions import StatisticalDistribution

class DistributionRegister:
    """
    Wrapper for registered distributions with safe access.
    """
    def __init__(self, stat_distributions: list[type[StatisticalDistribution]]):
        self._distributions = dict[str, StatisticalDistribution] = {}
        self._register_distributions(stat_distributions)

    def _register_distributions(self, stat_distributions: list[type[StatisticalDistribution]]):
        """Register all available GOF tests."""
        for dist in stat_distributions:
            dist_instance = dist()
            self._distributions[dist_instance.name] = dist_instance

    @property
    def distributions(self) -> List[str]:
        """Return list of available distribution names."""
        return list(self._distributions.keys())

    def get_dist(self, dist_name: str) -> Optional[type[StatisticalDistribution]]:
        """Return distribution class by name, or None if not found."""
        return self._distributions.get(dist_name)