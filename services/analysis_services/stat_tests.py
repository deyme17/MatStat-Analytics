from scipy.stats import ttest_1samp
import pandas as pd

class TestPerformer:
    """
    Utility for performing statistical tests.
    """
    @staticmethod
    def perform_t_test(sample: pd.Series, true_mean: float) -> dict:
        """
        Perform one-sample t-test comparing sample mean to true mean.
        Args:
            sample: input data
            true_mean: value to test against
        Return: 
            dictionary with t-statistic and p-value
        """
        t_stat, p_value = ttest_1samp(sample, popmean=true_mean)
        return {'t_statistic': t_stat, 'p_value': p_value}