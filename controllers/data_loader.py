from PyQt6.QtWidgets import QFileDialog
import os
from views.plot_graphs import plot_graphs

def load_data_file(window):
    """
    Load data from a file and update the application state.
    
    Args:
        window: The main application window
    """
    path, _ = QFileDialog.getOpenFileName(
        window,
        'Select the File',
        '',
        'All Supported Files (*.txt *.csv *.xlsx *.xls);;'
        'Text Files (*.txt);;'
        'CSV Files (*.csv);;'
        'Excel Files (*.xlsx *.xls);;'
        'All Files (*)'
    )

    if path:
        filename = os.path.basename(path)
        
        data = window.data_model.load_data(path)

        if data is not None and not data.empty:
            window.data = data
            window.data_processor.add_data(data, filename)
            
            # enable UI
            window.bins_spinbox.setEnabled(True)
            window.standardize_button.setEnabled(True)
            window.log_button.setEnabled(True)
            window.shift_spinbox.setEnabled(True)
            window.shift_button.setEnabled(True)
            window.data_version_combo.setEnabled(True)
            window.normal_anomaly_button.setEnabled(True)
            window.asymmetry_anomaly_button.setEnabled(True)
            
            # update data versions
            window.ui_controller.update_data_versions()
            
            # set default bins
            from utils.stat_func import set_default_bins
            window.bins_spinbox.setValue(set_default_bins(window.data))
            
            # plot
            plot_graphs(window)
            
            print(f'File {path} selected successfully')
        else:
            print(f'Failed to load file {path} or file is empty')