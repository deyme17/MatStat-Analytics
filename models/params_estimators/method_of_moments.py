from models.params_estimators.base_method import EstimationMethod

class MethodOfMoments(EstimationMethod):
    """Implements method of moments estimation for statistical distributions.
    
    This estimator matches sample moments to distribution moments
    to determine the optimal parameters.
    """
    
    @property
    def name(self) -> str:
        """Returns the name identifier for this estimation method.
        :return: Method name ('Method of moments')
        """
        return "Method of moments"

    def estimate(self, dist_instance, data):
        """Estimate distribution parameters using method of moments.
        
        :param dist_instance: Distribution instance to estimate parameters for
        :param data: Input data series for parameter estimation
        :return: Tuple of estimated parameters
        """
        return dist_instance.fit(data)