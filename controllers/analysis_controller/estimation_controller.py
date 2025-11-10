from models.params_estimators.base_method import EstimationMethod
from models.stat_distributions import StatisticalDistribution
from typing import Optional, List, Tuple, Dict
import pandas as pd


class ParameterEstimation:
    """
    Main controller class for parameter estimation operations.
    Provides a unified interface for estimating distribution parameters
    using different estimation methods.
    """
    def __init__(self, estimation_methods: List[EstimationMethod]):
        self._methods: Dict[str, EstimationMethod] = {}
        self._register_methods(estimation_methods)

    def _register_methods(self, estimation_methods: List[EstimationMethod]):
        """Register all available GOF tests."""
        for method in estimation_methods:
            self._methods[method.name] = method

    def estimate(self, dist: StatisticalDistribution, method_name: str, data: pd.Series) -> Optional[Tuple]:
        """
        Estimate parameters for a specified distribution using a chosen method.
        Args:
            dist: StatisticalDistribution to estimate (instance)
            method_name: Name of the estimation method to use
            data: Input data for parameter estimation
        Rerurn:
            Estimated parameters if successful, None otherwise
        """
        estimator = self._methods.get(method_name)
        if not estimator: 
            raise ValueError(f"Unknown estimation method: {method_name}")
        return estimator.estimate(dist, data)
    
    @property
    def methods(self) -> List[str]:
        return self._methods.keys()