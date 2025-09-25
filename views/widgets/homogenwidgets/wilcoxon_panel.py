from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel

class WilcoxonPanel(BaseHomoTestPanel):
    """
    Panel for Wilcoxon signed-rank test (paired samples).
    Displays test statistic, p-value, and decision.
    """
    def __init__(self, homogen_controller):
        stats = [
            {"key": "w_statistic", "label": "W-statistic"},
            {"key": "E[W]", "label": "Expected value of W"},
            {"key": "D[W]", "label": "Variance of W"},
            {"key": "w_value", "label": "Normalized W (w)"},
            {"key": "z_crit", "label": "Critical z"},
            {"key": "p_value", "label": "P-value"}
        ]
        super().__init__(homogen_controller, stats, 2, False)

    def get_test_name(self) -> str:
        return "wilcoxon test"