from models.graph_models import Hist
from models.stat_distributions.normal import NormalDistribution
from models.stat_distributions.exponential import ExponentialDistribution
from models.stat_distributions.weibull import WeibullDistribution
from models.stat_distributions.uniform import UniformDistribution
from models.stat_distributions.laplace import LaplaceDistribution
from utils.stat_func import variation_series, update_merged_table
import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chisquare, kstest

def plot_graphs(window):
    if window.data is None or window.data.empty:
        print("No data loaded or data is empty.")
        return

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
    normal_dist = NormalDistribution()
    exponential_dist = ExponentialDistribution()
    uniform_dist = UniformDistribution()
    weibull_dist = WeibullDistribution()
    laplace_dist = LaplaceDistribution()

    dist_mapping = {
        normal_dist: window.normal_dist_radio.isChecked(),
        exponential_dist: window.exponential_dist_radio.isChecked(),
        uniform_dist: window.uniform_dist_radio.isChecked(),
        weibull_dist: window.weibull_dist_radio.isChecked(),
        laplace_dist: window.laplace_dist_radio.isChecked()
    }
    
    # get the selected distribution
    selected_dist = None
    for dist, is_selected in dist_mapping.items():
        if is_selected:
            selected_dist = dist
            break
    
    # reset goodness-of-fit labels
    window.chi2_value_label.setText("statistic: , p-value: ")
    window.ks_value_label.setText("statistic: , p-value: ")
    
    # plot dists
    if selected_dist:
        try:
            selected_dist.plot(
                window.hist_ax, 
                data_no_nan,
            )
            
            # calc goodness-of-fit tests
            try:
                # fit
                params = selected_dist.fit(data_no_nan)
                
                # dist_obj
                dist_obj = selected_dist.get_distribution_object(params)
                
                if dist_obj is not None:
                    # hist
                    hist_counts, bin_edges = np.histogram(data_no_nan, bins=window.bins_spinbox.value())
                    
                    cdf_values = [dist_obj.cdf(edge) for edge in bin_edges]
                    expected_probs = np.diff(cdf_values)
                    expected_counts = expected_probs * len(data_no_nan)
                    
                    expected_counts = np.where(expected_counts < 1, 1, expected_counts)
                    expected_counts *= hist_counts.sum() / expected_counts.sum()

                    # chi-square test
                    chi2_stat, chi2_p = chisquare(hist_counts, expected_counts)
                    
                    # Kolmogorov-Smirnov test
                    ks_stat, ks_p = kstest(data_no_nan, dist_obj.cdf)
                    
                    window.chi2_value_label.setText(f"statistic: {chi2_stat:.4f}, p-value: {chi2_p:.4f}")
                    window.ks_value_label.setText(f"statistic: {ks_stat:.4f}, p-value: {ks_p:.4f}")

            except Exception as e:
                print(f"Error calculating goodness-of-fit tests: {str(e)}")
                window.chi2_value_label.setText(f"Error: {str(e)}")
                window.ks_value_label.setText(f"Error: {str(e)}")
            
        except Exception as e:
            window.show_error_message(f"{selected_dist.name} Distribution Error", 
                                   f"Could not plot {selected_dist.name} distribution: {str(e)}")

    window.hist_ax.legend(framealpha=0.5)
    window.hist_ax.set_xlabel('Value')
    window.hist_ax.set_ylabel('Frequency')
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
        window.edf_ax.set_xlabel('Value')
        window.edf_ax.set_ylabel('Cumulative Probability')
        window.edf_canvas.draw()

    except Exception as e:
        window.show_error_message("EDF Plot Error", 
                                f"Could not plot Empirical Distribution Function: {str(e)}")
    
    # update char table
    try:
        nan_count = window.data.isna().sum().sum()
        
        if nan_count > 0:
            nan_percentage = round((nan_count / window.data.size) * 100, 2)
            window.hist_ax.set_title(f'Histogram with Density Curve (Missing Values: {nan_count}, {nan_percentage}%)')
        
        # update the table
        update_merged_table(hist_model, data_no_nan, window.char_table, window)
    except Exception as e:
        window.show_error_message("Table Update Error", 
                                f"Could not update statistics table: {str(e)}")