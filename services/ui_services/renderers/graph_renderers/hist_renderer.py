import seaborn as sns
from services.ui_services.renderers.graph_renderers.graph_renderer import Renderer

class HistRenderer(Renderer):
    """
    Renderer for drawing histograms with optional KDE curve using seaborn.
    """
    @staticmethod
    def render(ax, data, bins: int, show_kde: bool):
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
        ax.grid(True, alpha=0.3)
        ax.set_title('Histogram')
        ax.set_xlabel('Values')
        ax.set_ylabel('Relative Frequency')
        ax.legend()