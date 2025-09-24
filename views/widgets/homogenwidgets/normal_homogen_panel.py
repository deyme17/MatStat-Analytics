from PyQt6.QtWidgets import QLabel
from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel
import pandas as pd

class NormalHomogenPanel(BaseHomoTestPanel):
    """
    Panel for Normal Homogeneity test with detailed statistics for variance and mean comparison.
    """
    def __init__(self, homogen_controller) -> None:
        """
        Initialize the Normal Homogeneity test panel.
        Args:
            homogen_controller (HomogenController): Controller for computing test values.
        """
        stats = [
            {"key": "f_statistic", "label": "F-statistic"},
            {"key": "p_value_var", "label": "P-value (variance)"},
            {"key": "var_consistent", "label": "Variance consistency"},
            {"key": "t_statistic", "label": "t-statistic"},
            {"key": "p_value_mean", "label": "P-value (mean)"},
            {"key": "mean_consistent", "label": "Mean consistency"},
            {"key": "type", "label": "Test type"}
        ]
        super().__init__(homogen_controller, stats)

    def get_test_name(self) -> str:
        """
        Get the name of the test for identification.
        Returns:
            str: Name of the normal homogeneity test.
        """
        return "normal homogeneity test"

    def evaluate(self, samples: list[pd.Series], alpha: float, is_independent: bool) -> None:
        """
        Evaluate the Normal Homogeneity test for two samples.
        Args:
            samples (list[pd.Series]): List of samples to test (should contain exactly 2 samples).
            alpha (float): Significance level.
            is_independent (bool): True if samples are independent, False if paired.
        """
        result = self.homogen_controller.run_2samples_test(
            test_name=self.get_test_name(),
            samples=samples,
            alpha=alpha,
            is_independent=is_independent
        )
        if not result:
            self.clear()
            return

        self.update_stats(result)