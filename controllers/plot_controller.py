from models.hist_model import Hist
from controllers.stat_func import variation_series, create_characteristic_table
from PyQt6.QtWidgets import QTableWidgetItem
import math
import numpy as np

def plot_histogram(window):
    if window.data is not None and not window.data.empty:
        # Create histogram
        hist_model = Hist(window.data, bins=window.bins_spinbox.value())
        variation_data = variation_series(window.data)
        print("\nVariation Series:")
        print(variation_data)

        # Plot histogram
        hist_model.plot_hist(ax=window.ax)
        
        # Update characteristics table
        update_characteristics_table(hist_model, window.char_table)
        
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


def update_characteristics_table(hist_model, table):
    # Get characteristics
    characteristics = create_characteristic_table(hist_model)
    
    # Update table
    table.setRowCount(len(characteristics))
    
    for idx, (name, value) in enumerate(characteristics.items()):
        table.setItem(idx, 0, QTableWidgetItem(str(name)))
        table.setItem(idx, 1, QTableWidgetItem(str(value)))