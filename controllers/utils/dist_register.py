from models.stat_distributions import BaseDistribution


class DistributionRegister:
    """
    Wrapper for registered distributions with safe access.
    """
    def __init__(self, stat_distributions: list[type[BaseDistribution]]):
        self._distributions: dict[str, BaseDistribution] = {}
        self._register_distributions(stat_distributions)

    def _register_distributions(self, stat_distributions: list[type[BaseDistribution]]):
        """Register all available GOF tests."""
        for dist in stat_distributions:
            self._distributions[dist().name] = dist

    @property
    def distributions(self) -> list[str]:
        """Return list of available distribution names."""
        return list(self._distributions.keys())

    def get_dist(self, dist_name: str) -> type[BaseDistribution] | None:
        """Return distribution class by name, or None if not found."""
        return self._distributions.get(dist_name)