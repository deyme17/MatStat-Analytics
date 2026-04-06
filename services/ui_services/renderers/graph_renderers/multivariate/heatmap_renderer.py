from numpy.random import sample
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
    def render(ax: plt.Axes, data: pd.DataFrame, max_rows: int = 100, seed: int = 42):
        """
        Render heatmap on the given Matplotlib axis.
        Args:
            ax (plt.Axes): Matplotlib axis to draw the heatmap on.
            data (pd.DataFrame): Input dataframe.
            max_rows (int): Maximum number of rows to use for heatmap (for performance).
            seed (int): Random seed for sampling if data exceeds max_rows.
        """        
        ax.clear()

        data_numeric = data.select_dtypes(include=[np.number])
        # for large datasets, sample a subset of rows to avoid performance issues with heatmap rendering
        if data_numeric.shape[0] > max_rows:
            ax.set_title(f"Heatmap (Normalized - Sampled {max_rows} rows)")
            data_numeric = data_numeric.sample(n=max_rows, random_state=seed)
        else:
            ax.set_title("Heatmap (Normalized)")

        data_norm = (data_numeric - data_numeric.min()) / (data_numeric.max() - data_numeric.min())
        sns.heatmap(
            data_norm,
            cmap="viridis",
            cbar=True,
            ax=ax
        )
        ax.set_xlabel("Features")
        ax.set_ylabel("Observations")