from models.hist_model import Hist
from controllers.stat_func import variation_series

def plot_histogram(window):
    if window.data is not None and not window.data.empty:
        window.ax.clear()

        # hist
        hist_model = Hist(window.data, bins=window.bins_spinbox.value())
        variation_data = variation_series(window.data)
        print("\nVariation Series:")
        print(variation_data)

        hist_model.plot_hist(ax=window.ax)
        window.canvas.draw()
    else:
        print("No data loaded or data is empty.")