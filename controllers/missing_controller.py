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
        """Update the data reference."""
        self.data = data
        self.update_missing_values_info()

    def update_missing_values_info(self):
        if self.data is not None:
            missing_info = detect_missing_values(self.data)
            self.window.missing_count_label.setText(f"Total Missing: {missing_info['total_missing']}")
            self.window.missing_percentage_label.setText(f"Missing Percentage: {missing_info['missing_percentage']:.2f}%")
    
    def impute_with_mean(self):
        if self.data is not None:
            self.data = replace_missing_with_mean(self.data)
            plot_graphs(self.window)
            self.update_missing_values_info()
            self.window.show_info_message("Success", "Missing values replaced with mean successfully.")
    
    def impute_with_median(self):
        if self.data is not None:
            self.data = replace_missing_with_median(self.data)
            plot_graphs(self.window)
            self.update_missing_values_info()
            self.window.show_info_message("Success", "Missing values replaced with median successfully.")
    
    def interpolate_missing(self, method):
        if self.data is not None:
            self.data = interpolate_missing_values(self.data, method)
            plot_graphs(self.window)
            self.update_missing_values_info()
            self.window.show_info_message("Success", f"Missing values interpolated ({method}) successfully.")
    
    def drop_missing_values(self):
        """New method to handle dropping missing values"""
        if self.data is not None:
            try:
                original_length = len(self.data)
                self.data = drop_missing_values(self.data)
                new_length = len(self.data)
                dropped_count = original_length - new_length
                
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