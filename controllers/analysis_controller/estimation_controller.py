from models.params_estimators import registered_estimation_methods
from models.stat_distributions import registered_distributions

class ParameterEstimation:
    """Main controller class for parameter estimation operations.
    
    Provides a unified interface for estimating distribution parameters
    using different estimation methods.
    """
    def __init__(self):
        """Initialize the parameter estimation service.
        Loads available estimation methods from registered_estimation_methods.
        """
        self.methods = registered_estimation_methods

    def estimate(self, dist_name: str, method_name: str, data):
        """Estimate parameters for a specified distribution using a chosen method.
        Args:
            dist_name: Name of the distribution to estimate (must be registered)
            method_name: Name of the estimation method to use
            data: Input data for parameter estimation

        Rerurn: 
            Estimated parameters if successful, None otherwise
        """
        dist_class = registered_distributions.get(dist_name)
        if not dist_class:
            return None

        dist_instance = dist_class()

        estimator = self.methods.get(method_name)
        if not estimator:
            return None

        return estimator.estimate(dist_instance, data)