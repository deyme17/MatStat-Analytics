import numpy as np

class DistributionRenderer:
    """
    Renderer for drawing theoretical distribution PDF curves on Matplotlib axes.
    """

    @staticmethod
    def render(ax, data, dist, color=None, label=None) -> bool:
        """
        Plot a fitted PDF curve of the given distribution on the provided axis.

        :param ax: Matplotlib axis to draw on
        :param data: pandas Series with input data
        :param dist: StatisticalDistribution instance to fit and render
        :param color: optional color override
        :param label: optional label for legend
        :return: True if rendering was successful, False otherwise
        """
        data_clean = data.dropna()
        if data_clean.empty:
            return False

        try:
            params = dist.fit(data_clean)
            x, pdf = dist.get_plot_data(data_clean, params)

            # Normalize PDF to histogram scale
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