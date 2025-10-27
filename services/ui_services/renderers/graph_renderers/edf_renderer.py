import numpy as np
import pandas as pd
from scipy import interpolate
from services.ui_services.renderers.graph_renderers.graph_renderer import Renderer

class EDFRenderer(Renderer):
    """
    Renderer for drawing the Empirical Distribution Function (EDF)
    as a step function and optional interpolated curve.
    """
    @staticmethod
    def render(ax, data: pd.Series, bin_edges: list[float] = None, show_edf_curve: bool = False, show_ogiva: bool = False):
        """
        Render the EDF on a given Matplotlib axis.
        Args:
            ax: Matplotlib axis to draw on
            data: pandas Series or NumPy array of values
            bin_edges: optional array of bin edges for step approximation
            show_edf_curve: whether to show a smoothed EDF curve
        """
        data = np.sort(data.dropna().values)
        n = len(data)

        if bin_edges is not None:
            bin_counts, _ = np.histogram(data, bins=bin_edges)
            cum_counts = np.cumsum(bin_counts)
            cum_rel_freq = cum_counts / cum_counts[-1] if cum_counts[-1] != 0 else np.zeros_like(cum_counts)

            for i in range(len(bin_edges) - 1):
                x = [bin_edges[i], bin_edges[i + 1]]
                y = [cum_rel_freq[i], cum_rel_freq[i]]
                ax.plot(x, y, 'c->', linewidth=2)
            ax.plot(bin_edges[-1], 1, 'c>', markersize=2, label="EDF")

        if show_edf_curve:
            y_edf = np.arange(1, n + 1) / n
            x_curve = np.linspace(data[0], data[-1], 300)
            f_interp = interpolate.interp1d(
                data, y_edf, kind='linear', bounds_error=False, fill_value=(0, 1)
            )
            y_interp = f_interp(x_curve)
            ax.plot(x_curve, y_interp, '-', color='c', label='EDF Curve', linewidth=2, alpha=0.4)

        if show_ogiva and bin_edges is not None:
            x = (bin_edges[:-1] + bin_edges[1:]) / 2
            y = cum_rel_freq
            ax.plot(x, y, 'o-', color='c', label='Ogiva', linewidth=2, alpha=0.4)

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel('Values')
        ax.set_ylabel('Probability')
        ax.set_title('Empirical Distribution Function')
        ax.grid(True, alpha=0.3)
        ax.legend()