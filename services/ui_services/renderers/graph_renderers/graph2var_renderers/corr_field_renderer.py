from services.ui_services.renderers.graph_renderers.graph_renderer import Renderer
from typing import Optional, Tuple
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class CorrelationFieldRenderer(Renderer):
    """
    Renderer for drawing correlation field for two columns of a DataFrame.
    """
    @staticmethod
    def render(ax: plt.Axes, df: pd.DataFrame, col_x: str, col_y: str, regression_coeffs: Optional[Tuple[float, float]] = None):
        """
        Render correlation field on the given Matplotlib axis.
        Args:
            ax: Matplotlib axis
            df: DataFrame with numeric columns
            col_x: first column name
            col_y: second column name
            regression_coeffs: optional coefficients (a, b) for regression line plotting
        """
        if col_x not in df or col_y not in df:
            raise ValueError(f"Columns {col_x} or {col_y} not found in DataFrame")
        ax.clear()

        x = df[col_x].to_numpy()
        y = df[col_y].to_numpy()

        # correlation field
        ax.scatter(x, y,
            c=y, cmap='viridis', s=40,
            alpha=0.7, edgecolors='w', linewidth=0.5
        )
        corr = df[col_x].corr(df[col_y])
        ax.text(0.05, 0.95, f'r={corr:.2f}', transform=ax.transAxes,
                fontsize=12, verticalalignment='top')
        
        # regression line
        if regression_coeffs is not None:
            a, b = regression_coeffs
            x_reg = np.linspace(x.min(), x.max(), 100)
            y_reg = a * x_reg + b
            ax.plot(x_reg, y_reg, color='r', linewidth=2, label=f'y = {a:.2f}x + {b:.2f}')
            ax.legend(loc='lower right', fontsize=10)

        ax.set_xlabel(col_x)
        ax.set_ylabel(col_y)
        ax.set_title('Correlation Field')

        ax.grid(False)