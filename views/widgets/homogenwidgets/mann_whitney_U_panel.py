from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel

class MannWhitneyUPanel(BaseHomoTestPanel):
    """
    Panel for Mann-Whitney U test test (paired samples).
    Displays test statistic, p-value, and decision.
    """
    def __init__(self, homogen_controller):
        stats = [
            {"key": "u_statistic", "label": "U-statistic"},
            {"key": "E[U]", "label": "Expected value of U"},
            {"key": "D[U]", "label": "Variance of U"},
            {"key": "u_value", "label": "Normalized U (u)"},
            {"key": "z_crit", "label": "Critical z"},
            {"key": "p_value", "label": "P-value"}
        ]
        super().__init__(homogen_controller, stats, 2, False)

    def get_test_name(self) -> str:
        return "mann-whitney U test"