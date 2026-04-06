import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
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
        ax.clear()

        data_numeric = data.select_dtypes(include=[np.number])
        scatter_matrix(
            data_numeric,
            ax=ax.figure.add_subplot(111),
            figsize=(6, 6),
            diagonal='hist',
            alpha=0.6,
        )
        ax.set_visible(False)