from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel

class BurtlettPanel(BaseHomoTestPanel):
    """
    Panel for Burtlett's test.
    Displays test statistic, p-value, and decision.
    """
    def __init__(self, homogen_controller):
        stats = [
            {"key": "S2", "label": "Intergroup Variation"},
            {"key": "chi2_statistic", "label": "Degrees of freedom"},
            {"key": "chi2_crit", "label": "Critical χ²"},
            {"key": "p_value", "label": "P-value"}
        ]
        super().__init__(homogen_controller, stats, None, True)

    def get_test_name(self) -> str:
        return "Burtlett test"