import numpy as np
import pandas as pd
from scipy.stats import t
from models.stat_distributions.stat_distribution import StatisticalDistribution

class SimulationService:
    """
    Service for simulating samples from distributions and evaluating T-tests.
    """
    def __init__(self, test_performer):
        """
        Initialize SimulationService with a StatisticsService instance.
        Args:
            test_performer: Service for performing statistical tests
        """
        self.test_performer = test_performer

    def generate_sample(self, distribution: StatisticalDistribution, size: int, params: dict) -> np.ndarray:
        """
        Generate a random sample from a distribution using the inverse CDF method.
        Args:
            distribution: instance of StatisticalDistribution
            size: number of values to generate
            params: distribution parameters
        Return:
            numpy array of sampled values
        """
        if not distribution.validate_params(): raise ValueError(f"Invalid parameters for {distribution.name}: {params}")
        u = np.random.uniform(0, 1, size)
        return distribution.get_inverse_cdf(u, params)

    def run_experiment(self, distribution: StatisticalDistribution, sizes: list[int], n_repeat: int,
                       true_mean: float, alpha: float = 0.05) -> list[dict]:
        """
        Run repeated T-tests on simulated samples of varying sizes.
        Args:
            distribution: instance of StatisticalDistribution
            sizes: list of sample sizes to test
            n_repeat: number of repetitions per sample size
            true_mean: theoretical mean to test against
            alpha: significance level for critical t-value
        Return:
            list of dictionaries with t-statistics summary and parameter estimates per sample size
        """
        results = []

        for size in sizes:
            t_stats = []
            param_estimates = []
            original_params = distribution.params

            for _ in range(n_repeat):
                sample = self.generate_sample(distribution, size, original_params)
                t_result = self.test_performer.perform_t_test(sample, true_mean=true_mean)
                t_stats.append(t_result['t_statistic'])
                dist_copy = type(distribution)()
                param_estimates.append(dist_copy.fit(pd.Series(sample)))

            distribution.params = original_params

            mean_t = np.mean(t_stats)
            std_t = np.std(t_stats, ddof=1)
            t_crit = t.ppf(1 - alpha / 2, df=size - 1)

            param_estimates = np.array(param_estimates) 
            params_mean = tuple(np.mean(param_estimates, axis=0)) 
            params_var = tuple(np.var(param_estimates, axis=0, ddof=1))

            results.append({
                'size': size,
                't_mean': mean_t,
                't_std': std_t,
                't_crit': t_crit,
                'params_mean': params_mean,
                'params_var': params_var
            })

        return results