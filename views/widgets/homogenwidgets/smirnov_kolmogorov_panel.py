from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel

class SmirnovKolmogorovPanel(BaseHomoTestPanel):
    """
    Panel for Smirnov-Kolmogorov test (paired samples).
    Displays test statistic, p-value, and decision.
    """
    def __init__(self, homogen_controller):
        stats = [
            {"key": "z_statistic", "label": "z-statistic"},
            {"key": "L_z", "label": "L(z)"},
            {"key": "z_crit", "label": "Critical z"},
            {"key": "p_value", "label": "P-value"}
        ]
        super().__init__(homogen_controller, stats, 2, True)

    def get_test_name(self) -> str:
        return "smirnov-kolmogorov test"