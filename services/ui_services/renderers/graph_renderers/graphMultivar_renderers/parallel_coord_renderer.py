import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates
from services.ui_services.renderers.graph_renderers.graph_renderer import Renderer


class ParallelCoordsRenderer(Renderer):
    """
    Renderer for drawing parallel coordinates plots for multivariate data visualization.
    """
    @staticmethod
    def render(ax: plt.Axes, data: pd.DataFrame, max_rows: int = 500, seed: int = 42):
        """
        Render parallel coordinates plot on the given Matplotlib axis.
        Args:
            ax (plt.Axes): Matplotlib axis to draw the plot on.
            data (pd.DataFrame): Input dataframe.
            max_rows (int): Maximum number of rows to use for parallel coordinates plot (for performance).
            seed (int): Random seed for sampling if data exceeds max_rows.
        """  
        ax.clear()

        data_numeric = data.select_dtypes(include=[np.number])
        # for large datasets, sample a subset of rows to avoid performance issues with heatmap rendering
        if len(data_numeric) > max_rows:
            ax.set_title(f"Parallel Coordinates (Sampled {max_rows} rows)")
            data_numeric = data_numeric.sample(n=max_rows, random_state=seed)
        else:
            ax.set_title("Parallel Coordinates")
        
        data_norm = (data_numeric - data_numeric.min()) / (data_numeric.max() - data_numeric.min())
        data_plot = data_norm.copy()
        data_plot["__dummy__"] = "all"

        parallel_coordinates(
            data_plot,
            class_column="__dummy__",
            ax=ax,
            color=["blue"],
            alpha=0.4
        )
        ax.get_legend().remove()
        ax.set_title("Parallel Coordinates Plot")
        ax.set_ylabel("Normalized values")
        ax.grid(True, linestyle='--', alpha=0.5)