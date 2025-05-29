import numpy as np
from scipy.stats import t
from models.stat_distributions.stat_distribution import StatisticalDistribution

class SimulationService:
    @staticmethod
    def generate_sample(distribution: StatisticalDistribution, size: int, params: dict) -> np.ndarray:
        """
        Generate a random sample from a distribution using the inverse CDF method.
        """
        u = np.random.uniform(0, 1, size)
        return distribution.get_inverse_cdf(u, params)
    
    @staticmethod
    def run_experiment(distribution: StatisticalDistribution, sizes: list[int], n_repeat: int, true_mean: float, alpha: float = 0.05) -> list[dict]:
        """
        Run repeated T-tests on samples generated from a distribution.
        """
        from services.analysis_services.statistics_service import StatisticsService
        results = []

        for size in sizes:
            t_stats = []
            for _ in range(n_repeat):
                sample = SimulationService.generate_sample(distribution, size, distribution.params)
                t_result = StatisticsService.perform_t_test(sample, true_mean=true_mean)
                t_stats.append(t_result['t_statistic'])

            mean_t = np.mean(t_stats)
            std_t = np.std(t_stats, ddof=1)
            t_crit = t.ppf(1 - alpha / 2, df=size - 1)

            results.append({
                'size': size,
                't_mean': mean_t,
                't_std': std_t,
                't_crit': t_crit
            })

        return results