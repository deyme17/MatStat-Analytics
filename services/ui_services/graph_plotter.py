import numpy as np
from scipy.stats import norm
from services.analysis_services.statistics_service import StatisticsService

class GraphPlotter:
    def __init__(self, panel):
        self.panel = panel
        self._cached_stats = {}

    def plot_all(self):
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
        model = self.panel.window.data_model
        show_kde = self.panel.show_additional_kde.isChecked()
        ax = self.panel.hist_ax
        ax.clear()

        hist_model = model.hist
        hist_model.plot_hist(ax, show_kde=show_kde)

        ax.set_facecolor('#f0f8ff')
        ax.grid(color='#b0e0e6', linestyle='--', alpha=0.7)
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        self.panel.hist_canvas.draw()

    def _draw_distribution_overlay(self):
        data = self.panel.data
        if data.isna().sum() > 0:
            return

        dist = self.panel.get_selected_distribution()
        if dist is None:
            return

        try:
            dist.plot(self.panel.hist_ax, data)
            params = dist.fit(data)
            dist_obj = dist.get_distribution_object(params)

            if dist_obj:
                stats = self._get_cached_stats(data)
                hist_counts, bin_edges = np.histogram(data, bins=self.panel.bins_spinbox.value())
                cdf_vals = [dist_obj.cdf(edge) for edge in bin_edges]
                expected_probs = np.diff(cdf_vals)
                expected_counts = np.where(expected_probs * stats['len'] < 1, 1, expected_probs * stats['len'])
                expected_counts *= hist_counts.sum() / expected_counts.sum()

        except Exception as e:
            print(f"Distribution Error: {e}")

        self.panel.hist_ax.legend(framealpha=0.5)
        self.panel.hist_canvas.draw()

    def _draw_distribution_cdf(self, ax, data):
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
        model = self.panel.window.data_model
        show_kde = self.panel.show_additional_kde.isChecked()
        ax = self.panel.edf_ax
        ax.clear()

        model.edf.plot(ax, bin_edges=model.hist.bin_edges, show_edf_curve=show_kde)
        self._draw_distribution_cdf(ax, model.series)

        ax.set_facecolor('#f0f8ff')
        ax.grid(color='#b0e0e6', linestyle='--', alpha=0.7)
        ax.set_xlabel('Value')
        ax.set_ylabel('Cumulative Probability')
        self.panel.edf_canvas.draw()

    def _get_cached_stats(self, data):
        data_id = id(data)
        if data_id not in self._cached_stats:
            self._cached_stats[data_id] = {
                'data': data,
                'len': len(data),
                'min': data.min(),
                'max': data.max()
            }
        return self._cached_stats[data_id]
