from services.ui_services.renderers.graph_renderers.graph_renderer import Renderer
import matplotlib.pyplot as plt
import pandas as pd


class CorrelationFieldRenderer(Renderer):
    """
    Renderer for drawing correlation field for two columns of a DataFrame.
    """
    @staticmethod
    def render(ax: plt.Axes, df: pd.DataFrame, col_x: str, col_y: str):
        """
        Render correlation field on the given Matplotlib axis.
        Args:
            ax: Matplotlib axis
            df: DataFrame with numeric columns
            col_x: first column name
            col_y: second column name
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
        
        ax.set_xlabel(col_x)
        ax.set_ylabel(col_y)
        ax.set_title('Correlation Field')

        ax.grid(False)