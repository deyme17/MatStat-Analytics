from services.graph_plotter import GraphPlotter
import pandas as pd

class GraphController:
    def __init__(self, panel):
        self.panel = panel
        self.plotter = GraphPlotter(panel)
        self.data = None

    def set_data(self, data: pd.Series):
        self.data = data
        self.panel.data = data
        if data is not None:
            self.plot_all()

    def plot_all(self):
        if self.data is not None and not self.data.empty:
            self.plotter.plot_all()

    def plot_histogram(self):
        if self.data is not None and not self.data.empty:
            self.plotter._draw_histogram(self.data)

    def plot_edf(self):
        if self.data is not None and not self.data.empty:
            self.plotter._draw_edf(self.data)

    def plot_overlay(self):
        if self.data is not None and not self.data.empty:
            self.plotter._draw_distribution_overlay(self.data)
