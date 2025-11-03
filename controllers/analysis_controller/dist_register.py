from models.stat_distributions import registered_distributions, StatisticalDistribution
from typing import List, Optional

class DistributionRegister:
    """
    Main controller class for parameter estimation operations.
    Provides a unified interface for estimating distribution parameters
    using different estimation methods.
    """
    def __init__(self):
        self._distributions = registered_distributions

    @property
    def distributions(self) -> List[str]:
        return self._distributions.keys()
    
    def get_dist(self, dist_name) -> Optional[StatisticalDistribution]:
        return self._distributions.get(dist_name, None)