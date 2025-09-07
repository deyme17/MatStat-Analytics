from PyQt6.QtWidgets import QLabel
import pandas as pd
from views.widgets.hypoteswidgets.gof_test_panel import BaseTestPanel
from models.stat_distributions.stat_distribution import StatisticalDistribution


class KolmogorovSmirnovPanel(BaseTestPanel):
    """
    Panel for Kolmogorov–Smirnov GOF test with detailed stats.
    """
    def __init__(self, gof_controller) -> None:
        """
        Initialize the Kolmogorov–Smirnov test panel.
        Args:
            gof_controller (GOFController): Controller to perform the test.
        """
        super().__init__("Kolmogorov–Smirnov Test", gof_controller)

        self.dn_label: QLabel = self.add_stat_label("Statistic (D₊): ")
        self.z_label: QLabel = self.add_stat_label("z = √n * D₊: ")
        self.critical_label: QLabel = self.add_stat_label("Critical z: ")
        self.p_label: QLabel = self.add_stat_label("P(z): ")

        self.finalize_layout()

    def evaluate(self, data: pd.Series, dist: StatisticalDistribution, alpha: float) -> None:
        """
        Perform Kolmogorov–Smirnov test and update panel.
        Args:
            data (pd.Series): Sample data to test.
            dist (StatisticalDistribution): Fitted distribution.
            alpha (float): Significance level.
        """
        result = self.gof_controller.run_test('ks', data, dist, alpha)
        if result is None:
            self.clear()
            return

        self.dn_label.setText(f"Statistic (D₊): {result['statistic']:.4f}")
        self.z_label.setText(f"z = √n * D₊: {result['extra']['z_stat']:.4f}")
        self.critical_label.setText(f"Critical z: {result['extra']['critical_value']:.4f}")
        self.p_label.setText(f"P(z): {result['p_value']:.4f}")

        self.update_result(result['passed'])