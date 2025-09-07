from PyQt6.QtWidgets import QLabel
import pandas as pd
from views.widgets.hypoteswidgets.gof_test_panel import BaseTestPanel
from models.stat_distributions.stat_distribution import StatisticalDistribution


class PearsonChi2Panel(BaseTestPanel):
    """
    Panel for Pearson's Chi-Squared GOF test with detailed stats.
    """
    def __init__(self, gof_controller) -> None:
        """
        Initialize the Pearson χ² test panel.
        Args:
            gof_controller (GOFController): Controller for computing test values.
        """
        super().__init__("Pearson Chi² Test", gof_controller)

        self.statistic_label: QLabel = self.add_stat_label("χ²: ")
        self.df_label: QLabel = self.add_stat_label("Degrees of freedom: ")
        self.critical_value_label: QLabel = self.add_stat_label("χ²(α, df): ")
        self.p_value_label: QLabel = self.add_stat_label("P(χ² ≤ x): ")

        self.finalize_layout()

    def evaluate(self, data: pd.Series, dist: StatisticalDistribution, alpha: float) -> None:
        """
        Evaluate the Pearson chi-squared test.
        Args:
            data (pd.Series): Observed data sample.
            dist (StatisticalDistribution): Theoretical distribution to test against.
            alpha (float): Significance level.
        """
        result = self.gof_controller.run_test('chi2', data, dist, alpha)
        if result is None:
            self.clear()
            return

        self.statistic_label.setText(f"χ²: {result['statistic']:.4f}")
        self.df_label.setText(f"Degrees of freedom: {result['extra']['df']}")
        self.critical_value_label.setText(f"χ²(α, df): {result['extra']['critical_value']:.4f}")
        self.p_value_label.setText(f"P(χ² ≤ x): {result['p_value']:.4f}")

        self.update_result(result['passed'])