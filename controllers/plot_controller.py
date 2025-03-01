from models.graph_models import Hist
from utils.stat_func import variation_series, create_characteristic_table, confidence_intervals
from PyQt6.QtWidgets import QTableWidgetItem
import math
import numpy as np

def plot_graphs(window):
    """
    Plot graphs and update data tables based on current data and settings.
    
    Args:
        window: The main application window
    """
    if window.data is not None and not window.data.empty:
        var_series = variation_series(window.data)
        #print(var_series)

        # hist
        hist_model = Hist(window.data, bins=window.bins_spinbox.value())
        
        # plot histogram
        window.hist_ax.clear()
        hist_model.plot_hist(ax=window.hist_ax)
        window.hist_canvas.draw()
        
        # plot EDF
        window.edf_ax.clear()
        hist_model.plot_EDF(ax=window.edf_ax)
        window.edf_canvas.draw()
        
        # update characteristics table
        update_merged_table(hist_model, window.data, window.char_table, window)


def update_merged_table(hist_model, data, table, window):
    """
    Update the statistical data and confidence intervals.
    
    Args:
        hist_model: The histogram model
        data: The data series
        table: The table widget to update
        window: The main application window
    """
    precision = window.precision_spinbox.value()
    confidence_level = window.confidence_spinbox.value()
    
    characteristics = create_characteristic_table(hist_model)
    ci = confidence_intervals(data, confidence_level=confidence_level, precision=precision)
    
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(['Value', 'Lower CI', 'Upper CI'])
    
    ci_mapping = {
        'Mean': 'Mean CI',
        'RMS deviation': 'Std Deviation CI',
        'Variance': 'Variance CI',
        'MED': 'MED CI',
        'Assymetry coeff.': 'Assymetry coeff. CI',
        'Excess': 'Excess CI'
    }
    
    rows = []
    for char_name, char_value in characteristics.items():
        ci_name = ci_mapping.get(char_name)
        
        if ci_name and ci_name in ci:
            ci_values = ci[ci_name]
            char_value = round(float(char_value), precision)
            rows.append((char_name, char_value, ci_values[0], ci_values[1]))
        else:
            rows.append((char_name, char_value, '-', '-'))
    
    # update table
    table.setRowCount(len(rows))
    for idx, (name, value, lower, upper) in enumerate(rows):
        # set header
        table.setVerticalHeaderItem(idx, QTableWidgetItem(str(name)))
        # set values
        table.setItem(idx, 0, QTableWidgetItem(str(value)))
        table.setItem(idx, 1, QTableWidgetItem(str(lower)))
        table.setItem(idx, 2, QTableWidgetItem(str(upper)))


def set_default_bins(data):
    """
    Calculate the default number of bins based on data size.
    
    Args:
        data: The data series
        
    Returns:
        int: The recommended number of bins
    """
    bins = 10

    if not data.empty:
        classes = len(data)

        if classes <= 100:
            bins = int(classes ** (1 / 2)) if classes % 2 == 1 else int(classes ** (1 / 2)) - 1
        else:
            bins = int(classes ** (1 / 3)) if classes % 2 == 1 else int(classes ** (1 / 3)) - 1

    return max(bins, 1)