from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel

class ANOVAPanel(BaseHomoTestPanel):
    """
    Panel for ANOVA test.
    Displays test statistic, p-value, and decision.
    """
    def __init__(self, homogen_controller):
        stats = [
            {"key": "S2_between", "label": "Intergroup Variation"},
            {"key": "S2_within", "label": "Within-group variation"},
            {"key": "S2_total", "label": "General variation"},
            {"key": "F_statistic", "label": "F-statistic"},
            {"key": "df1", "label": "Degrees of freedom V1"},
            {"key": "df2", "label": "Degrees of freedom V2"},
            {"key": "f_crit", "label": "Critical f"},
            {"key": "p_value", "label": "P-value"}
        ]
        super().__init__(homogen_controller, stats, None, True)

    def get_test_name(self) -> str:
        return "ANOVA test"