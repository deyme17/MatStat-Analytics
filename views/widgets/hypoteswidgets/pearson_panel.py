from PyQt6.QtWidgets import QLabel
from views.widgets.hypoteswidgets.gof_test_panel import BaseTestPanel
from funcs.gof_tests_comput.comput_chi import pearson_chi2_test

class PearsonChi2Panel(BaseTestPanel):
    def __init__(self, window):
        super().__init__("Pearson's χ² Test", window)

        self.statistic_label = self.add_stat_label("χ²: ")
        self.df_label = self.add_stat_label("Degrees of freedom: ")
        self.critical_value_label = self.add_stat_label("χ²(α, df): ")
        self.p_value_label = self.add_stat_label("P(χ² ≤ x): ")

        self.finalize_layout()

    def evaluate(self, data, dist, alpha):
        try:
            bins = self.window.graph_panel.bins_spinbox.value()
            result = pearson_chi2_test(data, dist, bins, alpha)

            self.statistic_label.setText(f"χ²: {result['statistic']:.4f}")
            self.df_label.setText(f"Degrees of freedom: {result['df']}")
            self.critical_value_label.setText(f"χ²(α={alpha:.2f}, df={result['df']}): {result['critical']:.4f}")
            self.p_value_label.setText(f"P(χ² ≤ x): {result['p_value']:.4f}")
            self.update_result(result["passed"])
        except Exception as e:
            self.statistic_label.setText(f"Error: {str(e)}")

    def clear(self):
        self.statistic_label.setText("χ²: ")
        self.df_label.setText("Degrees of freedom: ")
        self.critical_value_label.setText("χ²(α, df): ")
        self.p_value_label.setText("P(χ² ≤ x): ")
        super().clear()
