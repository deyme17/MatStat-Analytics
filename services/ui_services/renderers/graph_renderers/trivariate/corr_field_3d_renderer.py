import pandas as pd
import matplotlib.pyplot as plt
from services.ui_services.renderers.graph_renderers.graph_renderer import Renderer


class CorrField3dRenderer(Renderer):
    """
    Renderer for drawing correletion field plot for 3-variable data.
    """
    @staticmethod
    def render(ax: plt.Axes, df: pd.DataFrame, col_x: str, col_y: str, col_z: str):
        """
        Render correletion field plot 3D on the given Matplotlib axis.
        Args:
            ax: Matplotlib axis
            df: DataFrame with numeric columns
            col_x: first column name
            col_y: second column name
            col_z: third column name
        """
        if col_x not in df or col_y not in df or col_z not in df:
            raise ValueError(f"Columns {col_x}, {col_y}, or {col_z} not found in DataFrame")

        ax.clear()

        x = df[col_x].to_numpy()
        y = df[col_y].to_numpy()
        z = df[col_z].to_numpy()

        ax.scatter(
            x, y, z,
            alpha=0.6,
            edgecolors='w',
            linewidth=0.5,
            label=f"{col_x} vs {col_y} vs {col_z}",
            cmap="winter"
        )

        ax.set_xlabel(col_x)
        ax.set_ylabel(col_y)
        ax.set_zlabel(col_z)
        ax.set_title('Correletion field 3D')

        ax.grid(True, linestyle='--', alpha=0.5)