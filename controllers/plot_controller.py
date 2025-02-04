from models.hist_model import Hist
from controllers.stat_func import variation_series
import numpy as np
import math

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

def set_default_bins(data):
    bins = 10

    if not data.empty:
        classes = len(data)

        if classes <= 100:
            bins = int(classes ** (1 / 2)) if classes % 2 == 1 else int(classes ** (1 / 2)) - 1
        else:
            bins = int(classes ** (1 / 3)) if classes % 2 == 1 else int(classes ** (1 / 3)) - 1

    return max(bins, 1)
