class UIController:
    """Controller for UI interactions and data operations"""
    
    def __init__(self, window):
        """
        Initialize UI controller
        
        Args:
            window: Main application window
        """
        self.window = window
    
    def on_data_version_changed(self, index):
        """Handle data version change in dropdown"""
        window = self.window
        if index >= 0 and window.data_processor.get_current_data() is not None:
            window.data_processor.current_index = index
            window.data = window.data_processor.get_current_data()
            window.plot_button.setEnabled(True)
    
    def standardize_data(self):
        """Standardize the current data"""
        window = self.window
        if window.data is not None:
            # Only apply to original data
            orig_data = window.data_processor.get_original_data()
            
            # Check if "Standardized" already exists
            descriptions = window.data_processor.get_all_data_descriptions()
            if "Standardized" not in descriptions:
                window.data = window.data_processor.standardize_data(orig_data)
                self.update_data_versions()
            else:
                # Find and select existing standardized data
                index = descriptions.index("Standardized")
                window.data_version_combo.setCurrentIndex(index)
            
    def log_transform_data(self):
        """Apply logarithmic transformation to current data"""
        window = self.window
        if window.data is not None:
            # Only apply to original data
            orig_data = window.data_processor.get_original_data()
            
            # Check if any log transform already exists
            descriptions = window.data_processor.get_all_data_descriptions()
            log_exists = False
            log_index = -1
            
            for i, desc in enumerate(descriptions):
                if desc.startswith("Log("):
                    log_exists = True
                    log_index = i
                    break
                    
            if not log_exists:
                window.data = window.data_processor.log_transform_data(orig_data)
                self.update_data_versions()
            else:
                # Select existing log transform
                window.data_version_combo.setCurrentIndex(log_index)
            
    def shift_data(self):
        """Shift data by specified value"""
        window = self.window
        if window.data is not None:
            # Only apply to original data
            orig_data = window.data_processor.get_original_data()
            shift_value = window.shift_spinbox.value()
            
            # Check if this shift already exists
            descriptions = window.data_processor.get_all_data_descriptions()
            shift_exists = False
            shift_index = -1
            expected_description = f"Shifted by {shift_value}"
            
            for i, desc in enumerate(descriptions):
                if desc == expected_description:
                    shift_exists = True
                    shift_index = i
                    break
                    
            if not shift_exists:
                window.data = window.data_processor.shift_data(orig_data, shift_value)
                self.update_data_versions()
            else:
                # Select existing shift
                window.data_version_combo.setCurrentIndex(shift_index)
            
    def previous_data(self):
        """Navigate to previous data version"""
        window = self.window
        prev_data = window.data_processor.get_previous_data()
        if prev_data is not None:
            window.data = prev_data
            self.update_data_version_selection()
            window.plot_button.setEnabled(True)
            
    def next_data(self):
        """Navigate to next data version"""
        window = self.window
        next_data = window.data_processor.get_next_data()
        if next_data is not None:
            window.data = next_data
            self.update_data_version_selection()
            window.plot_button.setEnabled(True)
            
    def original_data(self):
        """Return to original data"""
        window = self.window
        orig_data = window.data_processor.get_original_data()
        if orig_data is not None:
            window.data = orig_data
            self.update_data_version_selection()
            window.plot_button.setEnabled(True)
            
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
            
            # Enable navigation buttons based on current position
            window.prev_button.setEnabled(window.data_processor.current_index > 0)
            window.next_button.setEnabled(
                window.data_processor.current_index < len(descriptions) - 1
            )
            window.original_button.setEnabled(window.data_processor.current_index > 0)
            
    def update_data_version_selection(self):
        """Update the selected data version in dropdown"""
        window = self.window
        if window.data_processor.current_index >= 0:
            window.data_version_combo.blockSignals(True)
            window.data_version_combo.setCurrentIndex(window.data_processor.current_index)
            window.data_version_combo.blockSignals(False)
            
            # Enable navigation buttons based on current position
            descriptions = window.data_processor.get_all_data_descriptions()
            window.prev_button.setEnabled(window.data_processor.current_index > 0)
            window.next_button.setEnabled(
                window.data_processor.current_index < len(descriptions) - 1
            )
            window.original_button.setEnabled(window.data_processor.current_index > 0)