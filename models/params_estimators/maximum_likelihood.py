from models.params_estimators.base_method import EstimationMethod
from scipy.optimize import minimize
import numpy as np

class MaximumLikelihoodMethod(EstimationMethod):
    """
    Implements maximum likelihood estimation for statistical distributions.
    This estimator finds parameters that maximize the likelihood function
    for the given data and distribution by minimizing the negative log-likelihood.
    """
    @property
    def name(self) -> str:
        """
        Returns: "Maximum Likelihood"
        """
        return "Maximum Likelihood"

    def estimate(self, dist_instance, data):
        """
        Estimate distribution parameters using maximum likelihood.
        Args:
            dist_instance: Distribution instance to estimate parameters for
            data: Input data series for parameter estimation
        Returns: 
            Tuple of estimated parameters if successful, None otherwise
        """
        def neg_log_likelihood(params, x, dist):
            """
            Negative log-likelihood function for optimization.
            Args:
                params: Current parameter values
                x: Input data values
                dist: Distribution instance
            Returns: 
                Negative log-likelihood value
            """
            try:
                pdf = dist.get_distribution_object(params).pdf(x)
                pdf = np.clip(pdf, 1e-10, None)
                return -np.sum(np.log(pdf))
            except:
                return np.inf

        x = data.dropna().values
        if len(x) == 0:
            return None

        try:
            initial_guess = dist_instance.fit(data)
        except:
            return None

        bounds = [(1e-10, None)] * len(initial_guess)

        try:
            result = minimize(
                neg_log_likelihood,
                initial_guess,
                args=(x, dist_instance),
                bounds=bounds,
                method='L-BFGS-B'
            )
            if result.success:
                return tuple(result.x)
        except:
            return None

        return None