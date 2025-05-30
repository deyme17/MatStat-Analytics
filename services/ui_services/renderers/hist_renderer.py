import seaborn as sns

class HistRenderer:
    """
    Renderer for drawing histograms with optional KDE curve using seaborn.
    """

    @staticmethod
    def render(ax, data, bins: int, show_kde: bool):
        """
        Render histogram on the given Matplotlib axis.

        :param ax: Matplotlib axis to draw on
        :param data: input data series or array
        :param bins: number of histogram bins
        :param show_kde: whether to display KDE curve
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