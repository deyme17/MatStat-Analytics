import numpy as np
from services.ui_services.renderers.graph_renderers.graph_renderer import Renderer

class DistributionRenderer(Renderer):
    """
    Renderer for drawing theoretical distribution PDF curves on Matplotlib axes.
    """

    @staticmethod
    def render(ax, data, dist, bins, color=None, label=None) -> bool:
        """
        Plot a fitted PDF curve of the given distribution on the provided axis.
        Args:
            ax: Matplotlib axis to draw on
            data: pandas Series with input data
            dist: StatisticalDistribution instance to fit and render
            bins: number of classes for PDF scaling
            color: optional color override
            label: optional label for legend
        Return:
            True if rendering was successful, False otherwise
        """
        data_clean = data.dropna()
        if data_clean.empty:
            return False

        try:
            params = dist.fit(data_clean)
            x, pdf = dist.get_plot_data(data_clean, params)

            # normalize pdf
            _, bin_edges = np.histogram(data_clean, bins=bins)
            bin_width = bin_edges[1] - bin_edges[0]
            pdf_scaled = pdf * bin_width

            ax.plot(x, pdf_scaled, color=color or dist.color,
                    label=label or f"{dist.name} Distribution")
            return True
        except Exception as e:
            print(f"[DistributionRenderer] Error: {e}")
            return False