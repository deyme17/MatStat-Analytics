from models.graph_models import Hist
from controllers.stat_func import variation_series, create_characteristic_table, confidence_intervals
from PyQt6.QtWidgets import QTableWidgetItem
import math
import numpy as np

def plot_graphs(window):
    if window.data is not None and not window.data.empty:
        # variation series
        var_series = variation_series(window.data)

        # hist
        hist_model = Hist(window.data, bins=window.bins_spinbox.value())
        window.hist_ax.clear()
        hist_model.plot_hist(ax=window.hist_ax)
        window.hist_canvas.draw()
        
        # EDF
        hist_model.plot_EDF(ax=window.edf_ax)
        window.edf_canvas.draw()
        
        # characteristics table
        update_characteristics_table(hist_model, window.char_table)
        
        # confidence intervals table
        update_confidence_intervals_table(window.data, window.ci_table)
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


def update_confidence_intervals_table(data, table):
    ci = confidence_intervals(data)
    
    table.setRowCount(len(ci))
    
    for idx, (name, value) in enumerate(ci.items()):
        table.setItem(idx, 0, QTableWidgetItem(str(name)))
        table.setItem(idx, 1, QTableWidgetItem(str(value[0])))  # Lower CI
        table.setItem(idx, 2, QTableWidgetItem(str(value[1])))  # Upper CI