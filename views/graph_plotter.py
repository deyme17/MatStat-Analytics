from funcs.stat_func import update_merged_table
from scipy.stats import chisquare, kstest
import numpy as np

class GraphPlotter:
    def __init__(self, window):
        self.window = window

    def plot_all(self):
        if self.window.data is None or self.window.data.empty:
            return

        data = self.window.data.dropna()
        if data.empty:
            self.window.show_error_message("Data Error", "All values are NaN.")
            return

        self._draw_histogram(data)
        self._draw_distribution_overlay(data)
        self._draw_edf(data)
        self._update_characteristics_table(data)

    def _draw_histogram(self, data):
        self.window.hist_ax.clear()
        from models.graph_model.hist_models import Hist
        hist_model = Hist(data, bins=self.window.bins_spinbox.value())
        hist_model.plot_hist(self.window.hist_ax)

        self.window.hist_ax.set_facecolor('#f0f8ff')
        self.window.hist_ax.grid(color='#b0e0e6', linestyle='--', alpha=0.7)
        self.window.hist_ax.set_xlabel('Value')
        self.window.hist_ax.set_ylabel('Frequency')
        self.window.hist_canvas.draw()

    def _draw_distribution_overlay(self, data):
        dist = self.window.dist_group.get_selected_distribution()
        self.window.chi2_value_label.setText("statistic: , p-value: ")
        self.window.ks_value_label.setText("statistic: , p-value: ")

        if dist is None:
            return

        try:
            dist.plot(self.window.hist_ax, data)
            params = dist.fit(data)
            dist_obj = dist.get_distribution_object(params)

            if dist_obj:
                hist_counts, bin_edges = np.histogram(data, bins=self.window.bins_spinbox.value())
                cdf_vals = [dist_obj.cdf(edge) for edge in bin_edges]
                expected_probs = np.diff(cdf_vals)
                expected_counts = np.where(expected_probs * len(data) < 1, 1, expected_probs * len(data))
                expected_counts *= hist_counts.sum() / expected_counts.sum()

                chi2_stat, chi2_p = chisquare(hist_counts, expected_counts)
                ks_stat, ks_p = kstest(data, dist_obj.cdf)

                self.window.chi2_value_label.setText(f"statistic: {chi2_stat:.4f}, p-value: {chi2_p:.4f}")
                self.window.ks_value_label.setText(f"statistic: {ks_stat:.4f}, p-value: {ks_p:.4f}")

        except Exception as e:
            self.window.show_error_message("Distribution Error", str(e))

        self.window.hist_ax.legend(framealpha=0.5)
        self.window.hist_canvas.draw()

    def _draw_edf(self, data):
        show_smooth = self.window.show_smooth_edf_checkbox.isChecked()
        confidence = self.window.confidence_spinbox.value()

        from models.graph_model.hist_models import Hist
        hist_model = Hist(data, bins=self.window.bins_spinbox.value())

        self.window.edf_ax.clear()
        hist_model.plot_EDF(self.window.edf_ax, show_smooth_edf=show_smooth, confidence_level=confidence)
        self.window.edf_ax.set_facecolor('#f0f8ff')
        self.window.edf_ax.grid(color='#b0e0e6', linestyle='--', alpha=0.7)
        self.window.edf_ax.set_xlabel('Value')
        self.window.edf_ax.set_ylabel('Cumulative Probability')
        self.window.edf_canvas.draw()

    def _update_characteristics_table(self, data):
        from models.graph_model.hist_models import Hist
        hist_model = Hist(data, bins=self.window.bins_spinbox.value())
        update_merged_table(hist_model, data, self.window.char_table, self.window)