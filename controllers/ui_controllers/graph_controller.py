import pandas as pd

class GraphController:
    """
    Controller for coordinating plotting, statistics, and confidence intervals in the graph panel.
    """
    def __init__(self, window, confidence_service):
        """
        Initialize the controller with references to UI panel and confidence service.
        :param window (QWidget): Reference to the main application window
        :param confidence_service: Service for computing confidence intervals
        """
        self.window = window
        self.panel = None
        self.confidence_service = confidence_service

    def set_data(self, series: pd.Series):
        """
        Sets the data to be plotted and triggers full update if data is valid.

        :param series: input pandas Series with numeric data
        """
        self.panel.data = series
        if series is not None and not series.empty:
            self.plot_all()

    def plot_all(self):
        """
        Triggers full redraw of all graph tabs, updates statistics and GOF tests.
        """
        self.panel.refresh_all()
        self.window.stat_controller.update_statistics_table()
        self.window.gof_tab.evaluate_tests()

    def on_distribution_changed(self):
        """
        Called when the selected distribution changes.
        Redraws graphs and re-runs Goodness-of-Fit tests.
        """
        if not self._valid():
            return

        self.panel.refresh_all()
        self.window.gof_tab.evaluate_tests()

    def on_bins_changed(self):
        """
        Called when the number of histogram bins is changed.
        Redraws graphs, updates statistics and GOF tests.
        """
        if not self._valid():
            return

        self.plot_all()

    def on_alpha_changed(self):
        """
        Called when the confidence level (alpha) is changed.
        Redraws graphs and updates GOF tests using the new confidence level.
        """
        if not self._valid():
            return

        self.panel.refresh_all()

    def on_kde_toggled(self):
        """
        Called when the KDE checkbox is toggled.
        Only redraws graphs without updating statistics or tests.
        """
        if not self._valid():
            return

        self.panel.refresh_all()

    def compute_cdf_with_ci(self, data: pd.Series, dist, confidence_level: float) -> tuple:
        """
        Compute the CDF and confidence interval bounds using the configured confidence service.
        :param data: Input pandas Series (cleaned numeric data)
        :param dist: Fitted statistical distribution instance
        :param confidence_level: Confidence level (e.g. 0.95)
        :return: Tuple of (x values, cdf, lower CI, upper CI), or None if computation failed
        """
        return self.confidence_service.cdf_variance_ci(data, dist, confidence_level)

    def _valid(self) -> bool:
        """
        Checks if the data model is valid and non-empty.

        :return: True if valid, False otherwise
        """
        return (
            self.window.data_model is not None and
            isinstance(self.window.data_model.series, pd.Series) and
            not self.window.data_model.series.empty
        )