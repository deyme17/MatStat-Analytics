from models.params_estimators.base_method import EstimationMethod

class MethodOfMoments(EstimationMethod):
    """
    Implements method of moments estimation for statistical distributions.
    This estimator matches sample moments to distribution moments
    to determine the optimal parameters.
    """
    @property
    def name(self) -> str:
        """
        Returns: "Method of moments"
        """
        return "Method of moments"

    def estimate(self, dist_instance, data):
        """
        Estimate distribution parameters using method of moments.
        Args:
            dist_instance: Distribution instance to estimate parameters for
            data: Input data series for parameter estimation
        Returns: 
            Tuple of estimated parameters
        """
        return dist_instance.fit(data)