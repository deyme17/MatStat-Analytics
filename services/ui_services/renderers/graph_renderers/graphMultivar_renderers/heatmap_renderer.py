import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from services.ui_services.renderers.graph_renderers.graph_renderer import Renderer


class HeatMapRenderer(Renderer):
    """
    Renderer for drawing heatmaps for multivariate data visualization.
    """
    @staticmethod
    def render(ax: plt.Axes, data: pd.DataFrame):
        """
        Render heatmap on the given Matplotlib axis.
        Args:
            ax (plt.Axes): Matplotlib axis to draw the heatmap on.
            data (pd.DataFrame): Input dataframe.
        """        
        ax.clear()

        data_numeric = data.select_dtypes(include=[np.number])
        data_norm = (data_numeric - data_numeric.min()) / (data_numeric.max() - data_numeric.min())
        sns.heatmap(
            data_norm,
            cmap="viridis",
            cbar=True,
            ax=ax
        )
        ax.set_title("Heatmap (normalized)")
        ax.set_xlabel("Features")
        ax.set_ylabel("Observations")