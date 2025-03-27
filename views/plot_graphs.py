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
        
        # Get which distributions to show
        dist_mapping = {
            'Normal': window.normal_dist_checkbox.isChecked(),
            'Exponential': window.exponential_dist_checkbox.isChecked(),
            'Uniform': window.uniform_dist_checkbox.isChecked() if hasattr(window, 'uniform_dist_checkbox') else False,
            'Weibull': window.weibull_dist_checkbox.isChecked() if hasattr(window, 'weibull_dist_checkbox') else False
        }
        
        # Determine if we should show any distributions
        any_distribution = any(dist_mapping.values())
        
        # Plot distributions if any selected
        if any_distribution:
            dist_handler = StatisticalDistributions()
            
            # Plot each selected distribution
            for dist_name, show_dist in dist_mapping.items():
                if show_dist:
                    try:
                        # Get appropriate color from handler
                        color = dist_handler.get_distribution_color(dist_name)
                        
                        # Plot the distribution
                        dist_handler.plot_distribution(
                            window.hist_ax, 
                            data_no_nan, 
                            dist_name, 
                            color=color,
                            linewidth=2, 
                            label=f'{dist_name}'
                        )
                    except Exception as e:
                        window.show_error_message(f"{dist_name} Distribution Error", 
                                               f"Could not plot {dist_name} distribution: {str(e)}")

        window.hist_ax.legend(framealpha=0.5)
        window.hist_canvas.draw()
        
        # plot EDF - use non-NaN values
        try:
            # Get smooth EDF checkbox state
            show_smooth_edf = window.show_smooth_edf_checkbox.isChecked() if hasattr(window, 'show_smooth_edf_checkbox') else True
            
            # Plot EDF with optional smooth curve
            hist_model.plot_EDF(window.edf_ax, show_smooth_edf=show_smooth_edf)
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