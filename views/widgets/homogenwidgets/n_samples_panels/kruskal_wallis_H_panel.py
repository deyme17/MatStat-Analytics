from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel

class HPanel(BaseHomoTestPanel):
    """
    Panel for Kruskal-Wallis H test.
    Displays test statistic, p-value, and decision.
    """
    def __init__(self, homogen_controller):
        stats = [
            {"key": "H_statistic", "label": "H-statistic"},
            {"key": "df", "label": "Degrees of freedom"},
            {"key": "xi2_crit", "label": "Critical χ²"}, 
            {"key": "p_value", "label": "P-value"}
        ]
        super().__init__(homogen_controller, stats, None, True)

    def get_test_name(self) -> str:
        return "H test"