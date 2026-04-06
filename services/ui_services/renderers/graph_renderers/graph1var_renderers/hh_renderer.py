import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from services.ui_services.renderers.graph_renderers.graph_renderer import Renderer
from models.stat_distributions import StatisticalDistribution


class HHRenderer(Renderer):
    """
    Renderer for drawing H-H plot (theoretical vs empirical quantiles).
    """
    @staticmethod
    def render(ax: plt.Axes, data: pd.Series, dist: StatisticalDistribution, 
               color: str = None, label: str = None) -> bool:
        """
        Plot H-H plot for the given distribution.
        Args:
            ax: Matplotlib axis to draw on
            data: pandas Series with input data
            dist: StatisticalDistribution instance to fit and render
            color: optional color override
            label: optional label for legend
        Return:
            True if rendering was successful, False otherwise
        """
        data_clean = data.dropna()
        if data_clean.empty or len(data_clean) < 2:
            return False
        try:
            params = dist.fit(data_clean)
            sorted_data = np.sort(data_clean)
            n = len(sorted_data)
            
            empirical_probs = (np.arange(1, n + 1) - 0.5) / n
            theoretical_quantiles = dist.get_inverse_cdf(empirical_probs, params)
            ax.scatter(theoretical_quantiles, sorted_data, 
                      alpha=0.6, color=color or dist.color,
                      label=label or f"{dist.name} H-H Plot", s=30
                      )
            # referance line
            min_val = min(theoretical_quantiles.min(), sorted_data.min())
            max_val = max(theoretical_quantiles.max(), sorted_data.max())
            ax.plot([min_val, max_val], [min_val, max_val], 
                   'k--', alpha=0.5, linewidth=1.5, label='Perfect Fit')
            
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('Theoretical Quantiles')
            ax.set_ylabel('Empirical Quantiles')
            ax.set_title('H-H Plot')
            ax.legend()
            
            return True
        except Exception as e:
            print(f"[HHRenderer] Error: {e}")
            return False