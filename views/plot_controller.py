from models.graph_models import Hist
from utils.stat_func import variation_series, update_merged_table
from models.stat_distributions import StatisticalDistributions

def plot_graphs(window):
    if window.data is not None and not window.data.empty:
        # variation series
        var_series = variation_series(window.data)

        # hist
        hist_model = Hist(window.data, bins=window.bins_spinbox.value())
        window.hist_ax.clear()
        
        hist_model.plot_hist(window.hist_ax, False, False)
        
        show_normal = window.normal_dist_checkbox.isChecked()
        show_exponential = window.exponential_dist_checkbox.isChecked()
        
        # stat distributions
        if show_normal or show_exponential:
            dist_handler = StatisticalDistributions()
            
            if show_normal:
                dist_handler.plot_distribution(window.hist_ax, window.data, 'Normal', color='r', label='Normal Distribution')
                
            if show_exponential:
                dist_handler.plot_distribution(window.hist_ax, window.data, 'Exponential', color='y', label='Exponential Distribution')

        
        window.hist_canvas.draw()
        
        # plot EDF
        hist_model.plot_EDF(window.edf_ax)
        window.edf_canvas.draw()
        
        # update characteristics table
        update_merged_table(hist_model, window.data, window.char_table, window)
    else:
        print("No data loaded or data is empty.")