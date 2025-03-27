from models.graph_models import Hist
from models.stat_distributions import StatisticalDistributions
from utils.stat_func import variation_series, update_merged_table
import pandas as pd
import numpy as np

def plot_graphs(window):
    if window.data is not None and not window.data.empty:
        # Make a copy of data without NaN for histogram and distributions
        data_no_nan = window.data.dropna()
        
        # Check if we have enough non-NaN data to proceed
        if len(data_no_nan) == 0:
            window.show_error_message("Data Error", "All values are missing (NaN). Cannot create plots.")
            return
        
        # variation series - can only use non-NaN values
        var_series = variation_series(data_no_nan)

        # hist - use non-NaN values for the histogram
        hist_model = Hist(data_no_nan, bins=window.bins_spinbox.value())
        window.hist_ax.clear()
        
        # style
        hist_model.plot_hist(window.hist_ax, False, False)
        window.hist_ax.set_facecolor('#f0f8ff')  # Light Blue Background
        window.hist_ax.grid(color='#b0e0e6', linestyle='--', alpha=0.7)
        
        show_normal = window.normal_dist_checkbox.isChecked()
        show_exponential = window.exponential_dist_checkbox.isChecked()
        
        # stat distributions - use non-NaN values
        if show_normal or show_exponential:
            dist_handler = StatisticalDistributions()
            
            try:
                if show_normal:
                    dist_handler.plot_distribution(window.hist_ax, data_no_nan, 'Normal', 
                                                color='r',  
                                                linewidth=2, 
                                                label='Normal Distribution')
            except Exception as e:
                window.show_error_message("Normal Distribution Error", 
                                           f"Could not plot normal distribution: {str(e)}")
                
            try:
                if show_exponential:
                    dist_handler.plot_distribution(window.hist_ax, data_no_nan, 'Exponential', 
                                                color='g',  
                                                linewidth=2, 
                                                label='Exponential Distribution')
            except Exception as e:
                window.show_error_message("Exponential Distribution Error", 
                                           f"Could not plot exponential distribution: {str(e)}")

        window.hist_ax.legend(framealpha=0.5)
        window.hist_canvas.draw()
        
        # plot EDF - use non-NaN values
        try:
            hist_model.plot_EDF(window.edf_ax)
            window.edf_ax.set_facecolor('#f0f8ff')
            window.edf_ax.grid(color='#b0e0e6', linestyle='--', alpha=0.7)
            window.edf_canvas.draw()
        except Exception as e:
            window.show_error_message("EDF Plot Error", 
                                       f"Could not plot Empirical Distribution Function: {str(e)}")
        
        # update characteristics table - use full data with NaN info
        try:
            # First display information about NaN values if any
            nan_count = window.data.isna().sum()
            if nan_count > 0:
                nan_percentage = round((nan_count / len(window.data)) * 100, 2)
                # Add info at the bottom of the plot
                window.hist_ax.set_title(f'Histogram with Density Curve (Missing Values: {nan_count}, {nan_percentage}%)')
            
            # Now update the table with non-NaN values
            update_merged_table(hist_model, data_no_nan, window.char_table, window)
        except Exception as e:
            window.show_error_message("Table Update Error", 
                                       f"Could not update statistics table: {str(e)}")
    else:
        print("No data loaded or data is empty.")