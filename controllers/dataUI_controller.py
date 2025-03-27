from views.plot_graphs import plot_graphs

class DataUIController:
    """Controller for UI interactions and data operations"""

    def __init__(self, window):
        self.window = window
        self.anomalies_removed = False

    def on_data_version_changed(self, index):
        """Handle data version change in dropdown"""
        window = self.window
        if 0 <= index < len(window.data_processor.data_history):
            window.data_processor.current_index = index
            window.data_processor.reset_transformation()
            window.data = window.data_processor.get_current_data()
            self.update_transformation_label()
            self.update_navigation_buttons()
            
            # Check for missing values before enabling operation buttons
            self.check_and_handle_missing_values()
            
            # Update missing data controller with new dataset
            window.missing_controller.update_data_reference(window.data)
                    
            plot_graphs(window)
    
    def check_and_handle_missing_values(self):
        """Check for missing values and update UI state accordingly"""
        window = self.window
        
        # Skip if data is not available
        if window.data is None:
            return
        
        # Check if data has missing values
        has_missing = window.data.isna().sum() > 0 if hasattr(window.data, 'isna') else False
        
        # Enable/disable data processing buttons based on missing values
        window.standardize_button.setEnabled(not has_missing)
        window.log_button.setEnabled(not has_missing)
        window.shift_spinbox.setEnabled(not has_missing)
        window.shift_button.setEnabled(not has_missing)
        window.normal_anomaly_button.setEnabled(not has_missing)
        window.asymmetry_anomaly_button.setEnabled(not has_missing)
        
        # Enable missing data panel buttons if missing values exist
        window.impute_mean_button.setEnabled(has_missing)
        window.impute_median_button.setEnabled(has_missing)
        window.interpolate_linear_button.setEnabled(has_missing)
        window.drop_missing_button.setEnabled(has_missing)

    def standardize_data(self):
        """Standardize the current data"""
        window = self.window
        if window.data is not None:
            current_data = window.data_processor.get_current_data()
            window.data = window.data_processor.standardize_data(current_data)
            self.update_transformation_label()
            self.update_navigation_buttons()
            
            # Update missing data controller
            window.missing_controller.update_data_reference(window.data)
            
            plot_graphs(window)

    def log_transform_data(self):
        """Apply logarithmic transformation to current data"""
        window = self.window
        if window.data is not None:
            current_data = window.data_processor.get_current_data()
            window.data = window.data_processor.log_transform_data(current_data)
            self.update_transformation_label()
            self.update_navigation_buttons()
            
            # Update missing data controller
            window.missing_controller.update_data_reference(window.data)
            
            plot_graphs(window)

    def shift_data(self):
        """Shift data by specified value"""
        window = self.window
        if window.data is not None:
            current_data = window.data_processor.get_current_data()
            shift_value = window.shift_spinbox.value()
            window.data = window.data_processor.shift_data(current_data, shift_value)
            self.update_transformation_label()
            self.update_navigation_buttons()
            
            # Update missing data controller
            window.missing_controller.update_data_reference(window.data)
            
            plot_graphs(window)

    def original_data(self):
        """Return to the original data state without transformations or anomalies."""
        window = self.window
        
        # Reset to orig data
        window.data_processor.reset_transformation()
        
        # Check if we have original data with missing values to restore
        if hasattr(window, 'original_data_with_missing'):
            window.data = window.original_data_with_missing.copy()
            
            # Update data in data_processor
            current_index = window.data_processor.current_index
            filename = window.data_processor.get_data_description().split(' (')[0]
            window.data_processor.data_history[current_index] = (filename, window.data.copy())
        
        # Restore from orig backup if exists (for anomalies)
        elif hasattr(window, 'original_data_backup'):
            window.data = window.original_data_backup.copy()
            
            # Update data in data_processor
            current_index = window.data_processor.current_index
            filename = window.data_processor.get_data_description().split(' (')[0]
            window.data_processor.data_history[current_index] = (filename, window.data.copy())
            
            # Remove backup
            delattr(window, 'original_data_backup')
        else:
            window.data = window.data_processor.get_original_data()
        
        if hasattr(self, 'anomalies_removed'):
            self.anomalies_removed = False
        
        # Update missing data controller
        window.missing_controller.update_data_reference(window.data)
        
        # Check for missing values in original data
        has_missing = window.data.isna().sum() > 0 if hasattr(window.data, 'isna') else False
        
        # Enable/disable operation buttons based on missing values
        window.standardize_button.setEnabled(not has_missing)
        window.log_button.setEnabled(not has_missing)
        window.shift_spinbox.setEnabled(not has_missing)
        window.shift_button.setEnabled(not has_missing)
        window.normal_anomaly_button.setEnabled(not has_missing)
        window.asymmetry_anomaly_button.setEnabled(not has_missing)
        
        # Enable missing data panel buttons if missing values exist
        window.impute_mean_button.setEnabled(has_missing)
        window.impute_median_button.setEnabled(has_missing)
        window.interpolate_linear_button.setEnabled(has_missing)
        window.drop_missing_button.setEnabled(has_missing)
        
        self.update_transformation_label()
        self.update_navigation_buttons()
        plot_graphs(window)

    def update_data_versions(self):
        """Update the available data versions in the dropdown"""
        window = self.window
        if window.data is not None:
            window.data_version_combo.blockSignals(True)
            window.data_version_combo.clear()
            descriptions = window.data_processor.get_all_data_descriptions()
            window.data_version_combo.addItems(descriptions)
            window.data_version_combo.setCurrentIndex(window.data_processor.current_index)
            window.data_version_combo.blockSignals(False)

            self.update_navigation_buttons()
            self.update_transformation_label()
            
            # Check for missing values
            self.check_and_handle_missing_values()

    def update_data_version_selection(self):
        """Update the selected data version in dropdown"""
        window = self.window
        if window.data_processor.current_index >= 0:
            window.data_version_combo.blockSignals(True)
            window.data_version_combo.setCurrentIndex(window.data_processor.current_index)
            window.data_version_combo.blockSignals(False)

            self.update_navigation_buttons()

    def update_transformation_label(self):
        """Update the transformation label to show current state"""
        window = self.window
        current_trans = window.data_processor.get_current_transformation()
        window.transformation_label.setText(f"Current state: {current_trans}")

    def is_transformed(self):
        """Check if data has been transformed."""
        return self.transformed_data is not None

    def update_navigation_buttons(self):
        """Updates navigation buttons."""
        window = self.window
        # enable original button if data has been transformed OR anomalies have been removed
        is_transformed = window.data_processor.transformed_data is not None
        
        # create a flag to track if anomalies were removed
        if not hasattr(self, 'anomalies_removed'):
            self.anomalies_removed = False
            
        window.original_button.setEnabled(is_transformed or self.anomalies_removed)