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
    def render(ax: plt.Axes, data: pd.DataFrame):
        ax.clear()

        data_numeric = data.select_dtypes(include=[np.number])
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