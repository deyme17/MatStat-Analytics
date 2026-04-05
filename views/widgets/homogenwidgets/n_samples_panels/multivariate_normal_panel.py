from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel

class MultiNormalPanel(BaseHomoTestPanel):
    def __init__(self, homogen_controller):
        stats = [
            {"key": "cov_statistic",  "label": "Cov V statistic"},
            {"key": "cov_critical",   "label": "Cov χ² critical"},
            {"key": "cov_df",         "label": "Cov degrees of freedom"},
            {"key": "cov_p_value",    "label": "Cov p-value"},
            {"key": "cov_decision",   "label": "Cov H₀ accepted"},
            {"key": "mean_statistic", "label": "Mean V statistic"},
            {"key": "mean_critical",  "label": "Mean χ² critical"},
            {"key": "mean_df",        "label": "Mean degrees of freedom"},
            {"key": "mean_p_value",   "label": "Mean p-value"},
            {"key": "mean_decision",  "label": "Mean H₀ accepted"},
        ]
        super().__init__(homogen_controller, stats, None, True, True)

    def get_test_name(self) -> str:
        return "Multivariate Normality Test"