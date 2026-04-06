import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from services.ui_services.renderers.graph_renderers.graph_renderer import Renderer


class HistogramMapRenderer(Renderer):
    """
    Renderer for drawing 3D histogram on 2D ax (as map) for two columns of a DataFrame.
    """
    @staticmethod
    def render(ax: plt.Axes, df: pd.DataFrame, col_x: str, col_y: str, bins1: int = 10, bins2: int = 10):
        """
        Render 3D histogram as heatmap on the given Matplotlib axis.
        Args:
            ax: Matplotlib axis
            df: DataFrame with numeric columns
            col_x: first column name
            col_y: second column name
            bins1: number of bins for X
            bins2: number of bins for Y
        Returns:
            colorbar
        """
        if col_x not in df or col_y not in df:
            raise ValueError(f"Columns {col_x} or {col_y} not found in DataFrame")
        ax.clear()

        x = df[col_x].to_numpy()
        y = df[col_y].to_numpy()

        hist, xedges, yedges = np.histogram2d(x, y, bins=[bins1, bins2])
        hist_rel = hist / hist.sum()

        mesh = ax.pcolormesh(xedges, yedges, hist_rel.T, shading='auto', cmap='viridis')
        cbar = plt.colorbar(mesh, ax=ax)
        cbar.set_label('Relative Frequency')

        ax.set_xlabel(col_x)
        ax.set_ylabel(col_y)
        ax.set_title('3D Histogram Map')

        ax.grid(False)
        return cbar