from services.ui_services.graph_plotter import GraphPlotter
import pandas as pd

class GraphController:
    """
    Controller for coordinating plotting of graphs on the visualization panel.
    """

    def __init__(self, panel):
        """
        :param panel: Reference to the UI panel that contains matplotlib axes and controls.
        """
        self.panel = panel
        self.plotter = GraphPlotter(panel)
        self.data_model = None
        self.window = panel.window

    def set_data(self, series: pd.Series):
        """
        Sets the data to be plotted and triggers full plotting if data is valid.

        :param series: Cleaned numerical data as a pandas Series.
        """
        self.panel.data = series
        if series is not None:
            self.plot_all()

    def plot_all(self):
        """
        Triggers rendering of all plot types:
        """
        if self.panel.data is not None and not self.panel.data.empty:
            self.plotter.plot_all()

    def plot_histogram(self):
        """
        Renders only the histogram plot.
        """
        if self.panel.data is not None and not self.panel.data.empty:
            self.plotter._draw_histogram(self.panel.data)

    def plot_edf(self):
        """
        Renders only the empirical distribution function (EDF) plot.
        """
        if self.panel.data is not None and not self.panel.data.empty:
            self.plotter._draw_edf(self.panel.data)

    def plot_overlay(self):
        """
        Renders only the theoretical distribution overlay on the histogram.
        """
        if self.panel.data is not None and not self.panel.data.empty:
            self.plotter._draw_distribution_overlay(self.panel.data)

    def evaluate_distribution_change(self):
        """
        Called when the distribution is changed in the graph panel.
        Updates plots and re-runs Goodness-of-Fit tests.
        """
        if self.window.data_model is None or self.window.data_model.series.empty:
            return
        self.panel.plot_all()
        selected_dist = self.panel.get_selected_distribution()
        if selected_dist is None:
            self.window.gof_tab.clear_tests()
        else:
            self.window.gof_tab.evaluate_tests()
