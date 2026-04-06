import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from utils.helpers import get_default_bin_count
from services.ui_services.renderers.graph_renderers.graph_renderer import Renderer


class ScatterMatrixRenderer(Renderer):
    """
    Renderer for drawing scatter matrix plots for multivariate data visualization.
    """
    @staticmethod
    def render(ax: plt.Axes, data: pd.DataFrame):
        """
        Render scatter matrix on the given Matplotlib axis.
        Args:
            ax (plt.Axes): Matplotlib axis to draw the scatter matrix on.
            data (pd.DataFrame): Input dataframe.
        """
        fig = ax.get_figure()
        fig.clf()

        data_numeric = data.select_dtypes(include=[np.number])
        if data_numeric.empty:
            new_ax = fig.add_subplot(111)
            new_ax.text(0.5, 0.5, "No numeric data for Scatter Matrix", ha='center')
            return

        n = len(data_numeric.columns)
        axes_grid_raw = fig.subplots(n, n)
        if n == 1:
            axes_grid_raw = np.array([[axes_grid_raw]])

        scatter_matrix(
            data_numeric,
            ax=axes_grid_raw,
            diagonal='hist',
            grid=True,
            marker='o',
            alpha=0.6,
            color='steelblue',
            edgecolor='white',
            linewidth=0.4,
            s=18,
            hist_kwds={
                'bins': get_default_bin_count(data_numeric),
                'color': 'steelblue',
                'edgecolor': 'black',
                'linewidth': 0.6,
                'alpha': 0.6,
            },
        )