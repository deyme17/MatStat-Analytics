import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from services.ui_services.renderers.graph_renderers.graph_renderer import Renderer


class BubblePlotRenderer(Renderer):
    """
    Renderer for drawing bubble plot (scatter plot with variable point sizes) for 3-variable data.
    """
    @staticmethod
    def render(ax: plt.Axes, df: pd.DataFrame, col_x: str, col_y: str, col_size: str):
        """
        Render bubble plot on the given Matplotlib axis.
        Args:
            ax: Matplotlib axis
            df: DataFrame with numeric columns
            col_x: first column name
            col_y: second column name
            col_size: third column name (for bubble sizes)
        """
        if col_x not in df or col_y not in df or col_size not in df:
            raise ValueError(f"Columns {col_x}, {col_y}, or {col_size} not found in DataFrame")

        ax.clear()

        x = df[col_x].to_numpy()
        y = df[col_y].to_numpy()
        size = df[col_size].to_numpy()

        # normalize
        min_size = 30
        max_size = 300
        size_scaled = min_size + (size - size.min()) / (size.max() - size.min()) * (max_size - min_size)

        ax.scatter(
            x, y,
            s=size_scaled,
            c=size,
            alpha=0.6,
            edgecolors='w',
            linewidth=0.5,
            label=f"{col_x} vs {col_y}"
        )

        ax.set_xlabel(col_x)
        ax.set_ylabel(col_y)
        ax.set_title('Bubble Plot')

        ax.legend(title=f"Size variable: {col_size}\nmin={size.min():.2f}, max={size.max():.2f}", loc='lower right', fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.5)