from utils.data_func import (
    detect_missing_values, 
    interpolate_missing_values, 
    replace_missing_with_mean, 
    replace_missing_with_median,
    drop_missing_values
)
from views.plot_graphs import plot_graphs
import numpy as np
from PyQt6.QtWidgets import QMessageBox

class MissingDataController:
    """Controller for handling missing data detection and removal."""
    
    def __init__(self, window):
        self.window = window
        self.data = None

    def update_data_reference(self, data):
        """Update the data reference and UI elements."""
        self.data = data
        self.update_missing_values_info()

    def update_missing_values_info(self):
        """Update the missing values information labels."""
        if self.data is not None:
            missing_info = detect_missing_values(self.data)
            self.window.missing_count_label.setText(f"Total Missing: {missing_info['total_missing']}")
            self.window.missing_percentage_label.setText(f"Missing Percentage: {missing_info['missing_percentage']:.2f}%")
    
    def _update_window_data(self, new_data):
        """Update the data in the window and data processor."""
        if self.data is not None:
            # Before updating, store original data with missing values if not already stored
            if not hasattr(self.window, 'original_data_with_missing'):
                self.window.original_data_with_missing = self.window.data_processor.get_original_data().copy()
            
            # Update the window's data reference
            self.window.data = new_data
            self.data = new_data
            
            # Update the data in the data processor
            current_index = self.window.data_processor.current_index
            if current_index >= 0:
                filename = self.window.data_processor.get_data_description()
                # Update the data in the history
                self.window.data_processor.data_history[current_index] = (filename, new_data.copy())
                # If there's a transformed version, update it as well
                if self.window.data_processor.transformed_data is not None:
                    self.window.data_processor.transformed_data = new_data.copy()
            
            # Enable operation buttons now that missing values are handled
            self._enable_operation_buttons()
            
            # Make sure original button is enabled now that we've modified the data
            self.window.original_button.setEnabled(True)
    
    def _enable_operation_buttons(self):
        """Enable data operation buttons after missing values have been handled."""
        # Check if we still have missing values
        has_missing = self.data.isna().sum() > 0 if hasattr(self.data, 'isna') else False
        
        # Enable/disable buttons based on missing values status
        self.window.standardize_button.setEnabled(not has_missing)
        self.window.log_button.setEnabled(not has_missing)
        self.window.shift_spinbox.setEnabled(not has_missing)
        self.window.shift_button.setEnabled(not has_missing)
        self.window.normal_anomaly_button.setEnabled(not has_missing)
        self.window.asymmetry_anomaly_button.setEnabled(not has_missing)
        
        # Update missing data panel buttons
        self.window.impute_mean_button.setEnabled(has_missing)
        self.window.impute_median_button.setEnabled(has_missing)
        self.window.interpolate_linear_button.setEnabled(has_missing)
        self.window.drop_missing_button.setEnabled(has_missing)
    
    def impute_with_mean(self):
        """Replace missing values with the mean of the dataset."""
        if self.data is not None:
            try:
                new_data = replace_missing_with_mean(self.data)
                self._update_window_data(new_data)
                plot_graphs(self.window)
                self.update_missing_values_info()
                self.window.show_info_message("Success", "Missing values replaced with mean successfully.")
            except Exception as e:
                self.window.show_error_message("Error", f"Failed to replace with mean: {str(e)}")
    
    def impute_with_median(self):
        """Replace missing values with the median of the dataset."""
        if self.data is not None:
            try:
                new_data = replace_missing_with_median(self.data)
                self._update_window_data(new_data)
                plot_graphs(self.window)
                self.update_missing_values_info()
                self.window.show_info_message("Success", "Missing values replaced with median successfully.")
            except Exception as e:
                self.window.show_error_message("Error", f"Failed to replace with median: {str(e)}")
    
    def interpolate_missing(self, method):
        """Interpolate missing values using the specified method."""
        if self.data is not None:
            try:
                new_data = interpolate_missing_values(self.data, method)
                self._update_window_data(new_data)
                plot_graphs(self.window)
                self.update_missing_values_info()
                self.window.show_info_message("Success", f"Missing values interpolated ({method}) successfully.")
            except Exception as e:
                self.window.show_error_message("Error", f"Failed to interpolate missing values: {str(e)}")
    
    def drop_missing_values(self):
        """Drop rows with missing values from the dataset."""
        if self.data is not None:
            try:
                original_length = len(self.data)
                new_data = drop_missing_values(self.data)
                new_length = len(new_data)
                dropped_count = original_length - new_length
                
                self._update_window_data(new_data)
                plot_graphs(self.window)
                self.update_missing_values_info()
                
                if dropped_count > 0:
                    self.window.show_info_message(
                        "Success", 
                        f"Dropped {dropped_count} rows with missing values.\n"
                        f"New dataset has {new_length} rows."
                    )
                else:
                    self.window.show_info_message("Info", "No rows with missing values found to drop.")
            except Exception as e:
                self.window.show_error_message("Error", f"Failed to drop missing values: {str(e)}")