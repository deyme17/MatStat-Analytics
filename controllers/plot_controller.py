from models.graph_models import Hist
from controllers.stat_func import variation_series, create_characteristic_table, confidence_intervals
from PyQt6.QtWidgets import QTableWidgetItem
import math
import numpy as np

def plot_graphs(window):
    if window.data is not None and not window.data.empty:
        # var series
        var_series = variation_series(window.data)
        print(var_series)

        # hist
        hist_model = Hist(window.data, bins=window.bins_spinbox.value())
        window.hist_ax.clear()
        hist_model.plot_hist(ax=window.hist_ax)
        window.hist_canvas.draw()
        
        # EDF
        hist_model.plot_EDF(ax=window.edf_ax)
        window.edf_canvas.draw()
        
        update_merged_table(hist_model, window.data, window.char_table)


def update_merged_table(hist_model, data, table):
    characteristics = create_characteristic_table(hist_model)
    ci = confidence_intervals(data)
    
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(['Value', 'Lower CI', 'Upper CI'])
    
    ci_mapping = {
        'Mean': 'Mean CI',
        'RMS deviation': 'Standard Deviation CI',
        'Variance': 'Variance CI',
        'Median': 'Median CI',
        'Assymetry coefficient': 'Skewness CI',
        'Excess': 'Excess CI'
    }
    
    rows = []
    for char_name, char_value in characteristics.items():
        ci_name = ci_mapping.get(char_name)
        if ci_name and ci_name in ci:
            ci_values = ci[ci_name]
            rows.append((char_name, char_value, ci_values[0], ci_values[1]))
        else:
            rows.append((char_name, char_value, '-', '-'))
    
    # update table
    table.setRowCount(len(rows))
    for idx, (name, value, lower, upper) in enumerate(rows):
        # header
        table.setVerticalHeaderItem(idx, QTableWidgetItem(str(name)))
        # vals
        table.setItem(idx, 0, QTableWidgetItem(str(value)))
        table.setItem(idx, 1, QTableWidgetItem(str(lower)))
        table.setItem(idx, 2, QTableWidgetItem(str(upper)))


def set_default_bins(data):
    bins = 10

    if not data.empty:
        classes = len(data)

        if classes <= 100:
            bins = int(classes ** (1 / 2)) if classes % 2 == 1 else int(classes ** (1 / 2)) - 1
        else:
            bins = int(classes ** (1 / 3)) if classes % 2 == 1 else int(classes ** (1 / 3)) - 1

    return max(bins, 1)