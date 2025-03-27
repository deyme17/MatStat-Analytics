from PyQt6.QtWidgets import QFileDialog
import os
from views.plot_graphs import plot_graphs
from utils.data_func import detect_missing_values

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
            # Store original data for potential restoration
            if not hasattr(window, 'original_data_with_missing'):
                window.original_data_with_missing = data.copy()
            
            window.data = data
            window.data_processor.add_data(data, filename)
            
            # Check for missing values
            missing_info = detect_missing_values(data)
            has_missing = missing_info['total_missing'] > 0
            
            # Enable/disable UI elements based on missing values
            window.bins_spinbox.setEnabled(True)
            window.data_version_combo.setEnabled(True)
            
            # Enable/disable operation buttons based on missing values
            window.standardize_button.setEnabled(not has_missing)
            window.log_button.setEnabled(not has_missing)
            window.shift_spinbox.setEnabled(not has_missing)
            window.shift_button.setEnabled(not has_missing)
            window.normal_anomaly_button.setEnabled(not has_missing)
            window.asymmetry_anomaly_button.setEnabled(not has_missing)
            
            # Enable missing data buttons if missing values exist
            window.impute_mean_button.setEnabled(has_missing)
            window.impute_median_button.setEnabled(has_missing)
            window.interpolate_linear_button.setEnabled(has_missing)
            window.drop_missing_button.setEnabled(has_missing)
            
            # Update data versions
            window.ui_controller.update_data_versions()
            
            # Update missing controller
            window.missing_controller.update_data_reference(window.data)
            
            # Set default bins
            from utils.stat_func import set_default_bins
            window.bins_spinbox.setValue(set_default_bins(window.data))
            
            # Show notification if missing values detected
            if has_missing:
                window.show_info_message(
                    "Missing Values Detected",
                    f"Found {missing_info['total_missing']} missing values ({missing_info['missing_percentage']:.2f}%).\n"
                    "Please handle missing values before performing data operations."
                )
            
            # Plot graphs
            plot_graphs(window)
            
            print(f'File {path} selected successfully')
        else:
            print(f'Failed to load file {path} or file is empty')