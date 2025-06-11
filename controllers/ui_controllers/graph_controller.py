import pandas as pd

class GraphController:
    """
    Controller for coordinating plotting of graphs on the visualization panel.
    """
    def __init__(self, panel):
        """
        Args:
            panel: Reference to the UI panel containing tabs and controls.
        """
        self.panel = panel
        self.window = panel.window

    def set_data(self, series: pd.Series):
        """
        Sets the data to be plotted and triggers full plotting if data is valid.
        """
        self.panel.data = series
        if series is not None and not series.empty:
            self.plot_all()

    def plot_all(self):
        """
        Triggers rendering of all active plot tabs.
        """
        self.panel.refresh_all()

    def evaluate_distribution_change(self):
        """
        Called when the distribution is changed in the graph panel.
        Updates plots and re-runs Goodness-of-Fit tests.
        """
        if self.window.data_model is None or self.window.data_model.series.empty:
            return

        self.plot_all()

        selected_dist = self.panel.get_selected_distribution()
        if selected_dist is None:
            self.window.gof_tab.clear_tests()
        else:
            self.window.gof_tab.evaluate_tests()
