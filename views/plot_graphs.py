from models.graph_models import Hist
from models.stat_distributions import StatisticalDistributions
from utils.stat_func import variation_series, update_merged_table
import pandas as pd
import numpy as np

def plot_graphs(window):
    if window.data is not None and not window.data.empty:
        data_no_nan = window.data.dropna()
        
        if len(data_no_nan) == 0:
            window.show_error_message("Data Error", "All values are missing (NaN). Cannot create plots.")
            return
        
        # get confidence level from UI
        confidence_level = window.confidence_spinbox.value()
        
        # variation series
        var_series = variation_series(data_no_nan)

        # hist
        hist_model = Hist(data_no_nan, bins=window.bins_spinbox.value())
        window.hist_ax.clear()
        
        # style
        hist_model.plot_hist(window.hist_ax, False, False)
        window.hist_ax.set_facecolor('#f0f8ff')
        window.hist_ax.grid(color='#b0e0e6', linestyle='--', alpha=0.7)
        
        # dists to show
        dist_mapping = {
            'Normal': window.normal_dist_checkbox.isChecked(),
            'Exponential': window.exponential_dist_checkbox.isChecked(),
            'Uniform': window.uniform_dist_checkbox.isChecked() if hasattr(window, 'uniform_dist_checkbox') else False,
            'Weibull': window.weibull_dist_checkbox.isChecked() if hasattr(window, 'weibull_dist_checkbox') else False
        }
        
        any_distribution = any(dist_mapping.values())
        
        # plot dists
        if any_distribution:
            dist_handler = StatisticalDistributions()
            
            for dist_name, show_dist in dist_mapping.items():
                if show_dist:
                    try:
                        color = dist_handler.get_distribution_color(dist_name)
                        
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
        
        # plot EDF
        try:
            show_smooth_edf = window.show_smooth_edf_checkbox.isChecked() if hasattr(window, 'show_smooth_edf_checkbox') else True
        
            hist_model.plot_EDF(
                window.edf_ax, 
                show_smooth_edf=show_smooth_edf,
                confidence_level=confidence_level
            )
            window.edf_ax.set_facecolor('#f0f8ff')
            window.edf_ax.grid(color='#b0e0e6', linestyle='--', alpha=0.7)
            window.edf_canvas.draw()
        except Exception as e:
            window.show_error_message("EDF Plot Error", 
                                    f"Could not plot Empirical Distribution Function: {str(e)}")
        
        # update char table
        try:
            nan_count = window.data.isna().sum()
            
            if nan_count > 0:
                nan_percentage = round((nan_count / len(window.data)) * 100, 2)
                window.hist_ax.set_title(f'Histogram with Density Curve (Missing Values: {nan_count}, {nan_percentage}%)')
            
            # update the table
            update_merged_table(hist_model, data_no_nan, window.char_table, window)
        except Exception as e:
            window.show_error_message("Table Update Error", 
                                    f"Could not update statistics table: {str(e)}")
    else:
        print("No data loaded or data is empty.")