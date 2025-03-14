from views.plot_controller import plot_graphs

class DataUIController:
    """Controller for UI interactions and data operations"""

    def __init__(self, window):
        self.window = window

    def on_data_version_changed(self, index):
        """Handle data version change in dropdown"""
        window = self.window
        if 0 <= index < len(window.data_processor.data_history):
            window.data_processor.current_index = index
            window.data_processor.reset_transformation()
            window.data = window.data_processor.get_current_data()
            self.update_transformation_label()
            self.update_navigation_buttons()
            
            window.normal_anomaly_button.setEnabled(True)
            window.asymmetry_anomaly_button.setEnabled(True)
                    
            plot_graphs(window)

    def standardize_data(self):
        """Standardize the current data"""
        window = self.window
        if window.data is not None:
            current_data = window.data_processor.get_current_data()
            window.data = window.data_processor.standardize_data(current_data)
            self.update_transformation_label()
            self.update_navigation_buttons()
            plot_graphs(window)

    def log_transform_data(self):
        """Apply logarithmic transformation to current data"""
        window = self.window
        if window.data is not None:
            current_data = window.data_processor.get_current_data()
            window.data = window.data_processor.log_transform_data(current_data)
            self.update_transformation_label()
            self.update_navigation_buttons()
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
            plot_graphs(window)

    def original_data(self):
        """Return to the original data state without transformations or anomalies."""
        window = self.window
        
        # handle reset after anomaly removal
        if hasattr(self, 'anomalies_removed') and self.anomalies_removed:
            if hasattr(window, 'original_data_backup'):
                # restore orig data
                window.data = window.original_data_backup.copy()
                
                # update the data in data_processor
                current_index = window.data_processor.current_index
                filename = window.data_processor.get_data_description()
                window.data_processor.data_history[current_index] = (filename, window.data.copy())
                
                # reset flags
                self.anomalies_removed = False
                delattr(window, 'original_data_backup')
                
                # enable anomaly buttons
                window.normal_anomaly_button.setEnabled(True)
                window.asymmetry_anomaly_button.setEnabled(True)
        
        # reset any transformations
        window.data_processor.reset_transformation()
        window.data = window.data_processor.get_current_data()
        self.update_transformation_label()
        
        # update the plots
        plot_graphs(window)
        
        # update navigation buttons state
        self.update_navigation_buttons()

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