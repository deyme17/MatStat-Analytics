import numpy as np
from scipy.stats import chisquare, kstest

class GraphPlotter:
    def __init__(self, panel):
        self.panel = panel

    def plot_all(self):
        data = self.panel.data
        if data is None or data.empty:
            return

        data = data.dropna()
        if data.empty:
            return

        self._draw_histogram(data)
        self._draw_distribution_overlay(data)
        self._draw_edf(data)

    def _draw_histogram(self, data):
        ax = self.panel.hist_ax
        ax.clear()

        from models.graph_model.hist_models import Hist
        hist_model = Hist(data, bins=self.panel.bins_spinbox.value())
        hist_model.plot_hist(ax)

        ax.set_facecolor('#f0f8ff')
        ax.grid(color='#b0e0e6', linestyle='--', alpha=0.7)
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        self.panel.hist_canvas.draw()

    def _draw_distribution_overlay(self, data):
        dist = self.panel.get_selected_distribution()
        if dist is None:
            return

        try:
            dist.plot(self.panel.hist_ax, data)
            params = dist.fit(data)
            dist_obj = dist.get_distribution_object(params)

            if dist_obj:
                hist_counts, bin_edges = np.histogram(data, bins=self.panel.bins_spinbox.value())
                cdf_vals = [dist_obj.cdf(edge) for edge in bin_edges]
                expected_probs = np.diff(cdf_vals)
                expected_counts = np.where(expected_probs * len(data) < 1, 1, expected_probs * len(data))
                expected_counts *= hist_counts.sum() / expected_counts.sum()

                chi2_stat, chi2_p = chisquare(hist_counts, expected_counts)
                ks_stat, ks_p = kstest(data, dist_obj.cdf)

        except Exception as e:
            print(f"Distribution Error: {e}")

        self.panel.hist_ax.legend(framealpha=0.5)
        self.panel.hist_canvas.draw()

    def _draw_edf(self, data):
        show_smooth = self.panel.show_smooth_edf_checkbox.isChecked()
        confidence = self.panel.confidence_spinbox.value()

        from models.graph_model.hist_models import Hist
        hist_model = Hist(data, bins=self.panel.bins_spinbox.value())

        ax = self.panel.edf_ax
        ax.clear()
        hist_model.plot_EDF(ax, show_smooth_edf=show_smooth, confidence_level=confidence)

        ax.set_facecolor('#f0f8ff')
        ax.grid(color='#b0e0e6', linestyle='--', alpha=0.7)
        ax.set_xlabel('Value')
        ax.set_ylabel('Cumulative Probability')
        self.panel.edf_canvas.draw()