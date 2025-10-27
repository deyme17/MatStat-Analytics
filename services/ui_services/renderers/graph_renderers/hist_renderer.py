import seaborn as sns
import numpy as np
import pandas as pd
from services.ui_services.renderers.graph_renderers.graph_renderer import Renderer

class HistRenderer(Renderer):
    """
    Renderer for drawing histograms with optional KDE curve using seaborn.
    """
    @staticmethod
    def render(ax, data: pd.Series, bins: int, show_kde: bool = False, freq_polygon: bool = False):
        """
        Render histogram on the given Matplotlib axis.
        Args:
            ax: Matplotlib axis to draw on
            data: input data series or array
            bins: number of histogram bins
            show_kde: whether to display KDE curve
        """
        ax.clear()
        sns.histplot(
            data, bins=bins, kde=show_kde, ax=ax,
            edgecolor='black', alpha=0.7, stat='probability', label='Histogram'
        )
        if freq_polygon:
            counts, bin_edges = np.histogram(data, bins=bins)
            rel_freq = counts / counts.sum()
            mids = (bin_edges[:-1] + bin_edges[1:]) / 2
            ax.plot(mids, rel_freq, '-o', color='c', label='Frequency Polygon', linewidth=2, alpha=0.4)

        ax.grid(True, alpha=0.3)
        ax.set_title('Histogram')
        ax.set_xlabel('Values')
        ax.set_ylabel('Relative Frequency')
        ax.legend()