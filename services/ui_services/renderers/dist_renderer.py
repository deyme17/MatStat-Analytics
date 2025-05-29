import numpy as np

class DistributionRenderer:
    @staticmethod
    def render(ax, data, dist, color=None, label=None):
        data_clean = data.dropna()
        if data_clean.empty:
            return False

        try:
            params = dist.fit(data_clean)
            x, pdf = dist.get_plot_data(data_clean, params)

            # Normalize to histogram scale
            hist_values, _ = np.histogram(data_clean, bins='auto', density=True)
            max_hist = np.max(hist_values) if len(hist_values) else 1
            max_pdf = np.max(pdf) if len(pdf) else 1
            if max_pdf > 0:
                pdf *= max_hist / max_pdf

            ax.plot(x, pdf, color=color or dist.color,
                    label=label or f"{dist.name} Distribution")
            return True
        except Exception as e:
            print(f"[DistributionRenderer] Error: {e}")
            return False
