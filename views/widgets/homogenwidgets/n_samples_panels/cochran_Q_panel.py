from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel

class CochranQPanel(BaseHomoTestPanel):
    """
    Panel for Cochran's Q test.
    Displays test statistic, p-value, and decision.
    """
    def __init__(self, homogen_controller):
        stats = [
            {"key": "Q_statistic", "label": "Q-statistic"},
            {"key": "df", "label": "Degrees of freedom"},
            {"key": "xi_crit", "label": "Critical χ²"},
            {"key": "p_value", "label": "P-value"}
        ]
        super().__init__(homogen_controller, stats, None, False)

    def get_test_name(self) -> str:
        return "Cochran Q test"