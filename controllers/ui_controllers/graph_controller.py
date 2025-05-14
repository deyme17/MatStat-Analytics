from services.ui_services.graph_plotter import GraphPlotter
import pandas as pd

class GraphController:
    def __init__(self, panel):
        self.panel = panel
        self.plotter = GraphPlotter(panel)
        self.data_model = None

    def set_data(self, series: pd.Series):
        self.panel.data = series
        if series is not None:
            self.plot_all()

    def plot_all(self):
        if self.panel.data is not None and not self.panel.data.empty:
            self.plotter.plot_all()

    def plot_histogram(self):
        if self.panel.data is not None and not self.panel.data.empty:
            self.plotter._draw_histogram(self.panel.data)

    def plot_edf(self):
        if self.panel.data is not None and not self.panel.data.empty:
            self.plotter._draw_edf(self.panel.data)

    def plot_overlay(self):
        if self.panel.data is not None and not self.panel.data.empty:
            self.plotter._draw_distribution_overlay(self.panel.data)