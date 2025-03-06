from controllers.plot_controller import plot_graphs

class UIController:
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
        """Return to original data"""
        window = self.window
        orig_data = window.data_processor.get_original_data()
        if orig_data is not None:
            window.data = orig_data
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

            window.original_button.setEnabled(window.data_processor.current_transformation != "Original")

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

    def update_navigation_buttons(self):
        """Updates navigation buttons"""
        window = self.window
        window.original_button.setEnabled(window.data_processor.is_transformed())