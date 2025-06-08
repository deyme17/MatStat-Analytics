from services.ui_services.renderers.hist_renderer import HistRenderer
from services.ui_services.renderers.edf_renderer import EDFRenderer
from services.ui_services.renderers.dist_renderer import DistributionRenderer
from services.analysis_services.statistics_service import StatisticsService
import numpy as np

class GraphPlotter:
    """
    Handles drawing of histogram, EDF, and distribution overlays on the graph panel.
    """

    def __init__(self, panel):
        """
        Initialize the plotter with the target graph panel.

        :param panel: custom graph panel containing axes and user controls
        """
        self.panel = panel
        self._cached_stats = {}  # internal cache for data stats

    def plot_all(self):
        """
        Plot histogram, EDF, and distribution overlay for current panel data.
        """
        data = self.panel.data
        if data is None or data.empty:
            return

        data = data.dropna()
        if data.empty:
            return

        self._cached_stats.clear()
        self._draw_histogram()
        self._draw_distribution_overlay()
        self._draw_edf()

    def _draw_histogram(self):
        """
        Draw histogram with optional KDE curve.
        """
        model = self.panel.window.data_model
        show_kde = self.panel.show_additional_kde.isChecked()
        ax = self.panel.hist_ax
        ax.clear()

        HistRenderer.render(ax, model.series, model.bins, show_kde)

        ax.set_facecolor('#f0f8ff')
        ax.grid(color='#b0e0e6', linestyle='--', alpha=0.7)
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        self.panel.hist_canvas.draw()

    def _draw_distribution_overlay(self):
        """
        Draw theoretical distribution curve over the histogram.
        """
        data = self.panel.data
        if data.isna().sum() > 0:
            return

        dist = self.panel.get_selected_distribution()
        if dist is None:
            return

        try:
            DistributionRenderer.render(self.panel.hist_ax, data, dist, bins=self.panel.window.data_model.hist.bins)
        except Exception as e:
            print(f"Distribution Error: {e}")

        self.panel.hist_ax.legend(framealpha=0.5)
        self.panel.hist_canvas.draw()

    def _draw_distribution_cdf(self, ax, data):
        """
        Draw statistical CDF with confidence intervals on the EDF plot.

        :param ax: target Matplotlib axis
        :param data: input data series
        """
        if data.isna().sum() > 0:
            return

        dist = self.panel.get_selected_distribution()
        if dist is None:
            return

        try:
            confidence = self.panel.confidence_spinbox.value()
            result = StatisticsService.get_cdf_with_confidence(data, dist, confidence)

            if result:
                x_vals, cdf_vals, lower_ci, upper_ci = result
                ax.plot(x_vals, cdf_vals, '-', color=dist.color, label=f'{dist.name} CDF', linewidth=2)
                ax.fill_between(x_vals, lower_ci, upper_ci, color='pink', alpha=0.2,
                                label=f"Confidence level: {confidence * 100:.0f}%")

                ax.legend()
                ax.set_title("EDF and Statistical CDF with Confidence Interval")
                ax.set_ylim(-0.05, 1.05)

        except Exception as e:
            print(f"Error in CDF overlay: {e}")
            ax.clear()
            ax.text(0.5, 0.5, f"Error plotting CDF: {str(e)}", ha='center', va='center', transform=ax.transAxes)

    def _draw_edf(self):
        """
        Draw Empirical Distribution Function (EDF) and overlay theoretical CDF.
        """
        model = self.panel.window.data_model
        show_kde = self.panel.show_additional_kde.isChecked()
        ax = self.panel.edf_ax
        ax.clear()

        EDFRenderer.render(ax, model.series, bin_edges=model.hist.bin_edges, show_edf_curve=show_kde)
        self._draw_distribution_cdf(ax, model.series)

        ax.set_facecolor('#f0f8ff')
        ax.grid(color='#b0e0e6', linestyle='--', alpha=0.7)
        ax.set_xlabel('Value')
        ax.set_ylabel('Cumulative Probability')
        self.panel.edf_canvas.draw()

    def _get_cached_stats(self, data):
        """
        Cache and return basic stats for the given data object.

        :param data: input data series
        :return: dictionary with length, min, max
        """
        data_id = id(data)
        if data_id not in self._cached_stats:
            self._cached_stats[data_id] = {
                'data': data,
                'len': len(data),
                'min': data.min(),
                'max': data.max()
            }
        return self._cached_stats[data_id]