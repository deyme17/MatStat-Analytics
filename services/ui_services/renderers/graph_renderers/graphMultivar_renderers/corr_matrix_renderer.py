import seaborn as sns
import numpy as np
import pandas as pd
from typing import Callable, Optional
import matplotlib.pyplot as plt
from services.ui_services.renderers.graph_renderers.graph_renderer import Renderer
from models.correlation_coeffs._significance_test_result import SignificanceTestResult


class CorrMatrixRenderer(Renderer):
    """
    Renderer for drawing correlation matrices using seaborn heatmap.
    """
    @staticmethod
    def render(ax: plt.Axes, data: pd.DataFrame, corr_callable: Callable[[str, pd.Series, pd.Series], float], 
               corr_name: str, annot: bool = True, cmap: str = "viridis", 
               significance_callable: Optional[Callable[[str, pd.Series, pd.Series, float], SignificanceTestResult]] = None, 
               alpha: float = 0.05,):
        """
        Render correlation matrix on the given Matplotlib axis.
        Args:
            ax (plt.Axes): Matplotlib axis to draw the heatmap on.
            data (pd.DataFrame): Input dataframe.
            corr_callable (callable): Function to compute correlation between two arrays.
                                      Should accept (x: pd.Series, y: pd.Series) and return float.
            corr_name (str): Name of the correlation coefficient
            annot (bool): Whether to annotate the heatmap with coefficient values.
            cmap (str): Color map to use for heatmap.
            significance_callable: Optional function (corr_name, x, y, alpha) -> SignificanceTestResult
            alpha: Significance level used when significance_callable is not None.
        """
        columns = data.columns
        n = len(columns)
        corr_matrix = np.zeros((n, n))
        mask = np.zeros((n, n), dtype=bool)

        for i, col1 in enumerate(columns):
            for j, col2 in enumerate(columns):
                if i == j:
                    corr_matrix[i, j] = 1.0
                    continue

                corr_matrix[i, j] = corr_callable(corr_name, data[col1], data[col2])

                if significance_callable is not None:
                    result = significance_callable(corr_name, data[col1], data[col2], alpha)
                    if not result.is_significant:
                        mask[i, j] = True

        corr_df = pd.DataFrame(corr_matrix, index=columns, columns=columns)
        sns.heatmap(
            corr_df,
            annot=annot,
            cmap=cmap,
            ax=ax,
            vmin=-1,
            vmax=1,
            mask=mask,
        )
        title = "Correlation Matrix"
        if corr_name:
            title += f" ({corr_name})"
        if significance_callable is not None:
            title += f" [α={alpha}]"
        ax.set_title(title)