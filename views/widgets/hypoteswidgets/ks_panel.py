from PyQt6.QtWidgets import QLabel
from views.widgets.hypoteswidgets.gof_test_panel import BaseTestPanel
from funcs.gof_tests_comput.comput_ks import kolmogorov_smirnov_test

class KolmogorovSmirnovPanel(BaseTestPanel):
    def __init__(self, window):
        super().__init__("Kolmogorov-Smirnov Test (Refined)", window)

        self.dn_label = self.add_stat_label("Statistic (Dₙ): ")
        self.z_label = self.add_stat_label("z = √n * Dₙ: ")
        self.critical_label = self.add_stat_label("Critical z: ")
        self.p_label = self.add_stat_label("P(z): ")

        self.finalize_layout()

    def evaluate(self, data, dist, alpha):
        try:
            result = kolmogorov_smirnov_test(data, dist, alpha)

            self.dn_label.setText(f"Statistic (Dₙ): {result['dn']:.4f}")
            self.z_label.setText(f"z = √n * Dₙ: {result['z']:.4f}")
            self.critical_label.setText(f"Critical z(α={alpha:.2f}): {result['critical']:.4f}")
            self.p_label.setText(f"P(z): {result['p_value']:.4f}")
            self.update_result(result["passed"])
        except Exception as e:
            self.dn_label.setText(f"Error: {str(e)}")

    def clear(self):
        self.dn_label.setText("Statistic (Dₙ): ")
        self.z_label.setText("z = √n * Dₙ: ")
        self.critical_label.setText("Critical z: ")
        self.p_label.setText("P(z): ")
        super().clear()

