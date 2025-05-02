from PyQt6.QtWidgets import QFileDialog
import os
from views.graph_plotter import GraphPlotter
from funcs.data_func import detect_missing_values

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
            # store original data
            if not hasattr(window, 'original_data_with_missing'):
                window.original_data_with_missing = data.copy()
            
            window.data = data
            window.data_processor.add_data(data, filename)
            
            # check for missing vals
            missing_info = detect_missing_values(data)
            has_missing = missing_info['total_missing'] > 0
            
            # enable/disable UI
            window.bins_spinbox.setEnabled(True)
            window.data_version_combo.setEnabled(True)
            
            # enable/disable operation buttons
            window.standardize_button.setEnabled(not has_missing)
            window.log_button.setEnabled(not has_missing)
            window.shift_spinbox.setEnabled(not has_missing)
            window.shift_button.setEnabled(not has_missing)
            window.normal_anomaly_button.setEnabled(not has_missing)
            window.asymmetry_anomaly_button.setEnabled(not has_missing)
            window.confidence_anomaly_button.setEnabled(not has_missing)
            window.anomaly_gamma_spinbox.setEnabled(not has_missing)
            
            # enable missing data buttons
            window.impute_mean_button.setEnabled(has_missing)
            window.impute_median_button.setEnabled(has_missing)
            window.interpolate_linear_button.setEnabled(has_missing)
            window.drop_missing_button.setEnabled(has_missing)
            
            # update data versions
            window.ui_controller.update_data_versions()
            
            # update missing controller
            window.missing_controller.update_data_reference(window.data)
            
            # set default bins
            from funcs.stat_func import set_default_bins
            window.bins_spinbox.setValue(set_default_bins(window.data))
            
            # notify about missings
            if has_missing:
                window.show_info_message(
                    "Missing Values Detected",
                    f"Found {missing_info['total_missing']} missing values ({missing_info['missing_percentage']:.2f}%).\n"
                    "Please handle missing values before performing data operations."
                )
            
            # plot graphs
            GraphPlotter(window).plot_all()
            
            print(f'File {path} selected successfully')
        else:
            print(f'Failed to load file {path} or file is empty')