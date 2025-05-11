import numpy as np
from scipy import interpolate, stats
from scipy.ndimage import gaussian_filter1d

class EmpiricalDistribution:
    def __init__(self, data):
        if hasattr(data, 'dropna'):
            self.data = np.sort(data.dropna().values)
        else:
            self.data = np.sort(data[~np.isnan(data)])

        if len(self.data) == 0:
            raise ValueError("No valid data points for EDF")

    def plot(self, ax, bin_edges=None, show_smooth_edf=True, confidence_level=0.95):
        try:
            n = len(self.data)
            alpha = 1 - confidence_level

            if bin_edges is not None:
                bin_counts, _ = np.histogram(self.data, bins=bin_edges)
                cum_counts = np.cumsum(bin_counts)
                cum_rel_freq = cum_counts / cum_counts[-1]

                for i in range(len(bin_edges) - 1):
                    x = [bin_edges[i], bin_edges[i + 1]]
                    y = [cum_rel_freq[i], cum_rel_freq[i]]
                    ax.plot(x, y, 'c->', linewidth=2)

                ax.plot(bin_edges[-1], 1, 'c>', markersize=2)

            if show_smooth_edf:
                y_edf = np.arange(1, n + 1) / n
                x_smooth = np.linspace(self.data.min(), self.data.max(), 300)

                f_interp = interpolate.interp1d(self.data, y_edf, kind='linear',
                                                bounds_error=False, fill_value=(0, 1))
                y_interp = f_interp(x_smooth)

                y_smooth = gaussian_filter1d(y_interp, sigma=8)
                y_smooth = np.clip(y_smooth, 0, 1)

                ax.plot(x_smooth, y_smooth, '-', color='red', label='EDF Smooth', linewidth=2)

                # confidence band
                u = stats.norm.ppf(1 - alpha / 2)
                dispersion = 0.25 / n
                ci_width = u * np.sqrt(dispersion)
                ax.fill_between(
                    x_smooth,
                    np.clip(y_smooth - ci_width, 0, 1),
                    np.clip(y_smooth + ci_width, 0, 1),
                    color='skyblue',
                    alpha=0.3,
                    label=f"{confidence_level * 100:.0f}% CI"
                )

            ax.set_ylim(-0.05, 1.05)
            ax.set_xlabel('Values')
            ax.set_ylabel('Probability')
            ax.set_title('Empirical Distribution Function')
            ax.grid(True, alpha=0.3)

            handles, labels = ax.get_legend_handles_labels()
            if handles:
                ax.legend()

            ax.figure.tight_layout()
            ax.figure.canvas.draw()

        except Exception as e:
            ax.clear()
            ax.text(0.5, 0.5, f"Error plotting EDF: {str(e)}", ha='center', va='center', transform=ax.transAxes)
            ax.figure.canvas.draw()