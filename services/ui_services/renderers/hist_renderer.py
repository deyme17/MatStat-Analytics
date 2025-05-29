import seaborn as sns

class HistRenderer:
    @staticmethod
    def render(ax, data, bins, show_kde):
        ax.clear()
        sns.histplot(data, bins=bins, kde=show_kde, ax=ax,
                     edgecolor='black', alpha=0.7, stat='probability', label='Histogram')
        ax.grid(True, alpha=0.3)
        ax.set_title('Histogram')
        ax.set_xlabel('Values')
        ax.set_ylabel('Relative Frequency')
        ax.legend()