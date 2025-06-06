class DataVersionController:
    """
    Controller for managing dataset versions (original and transformed).
    """

    def __init__(self, window):
        """        
        Args:
            window (QWidget): Reference to the main application window
        """
        self.window = window

    def on_data_version_changed(self, index):
        """
        Called when the user selects a different version from the dropdown.

        :param index: Index of the selected version in the dropdown.
        """
        labels = self.window.version_manager.get_all_descriptions()
        if 0 <= index < len(labels):
            label = labels[index]
            self.window.version_manager.switch_to(label)
            self.window.data_model = self.window.version_manager.get_current_data()
            self._update_all()

    def original_data(self):
        """
        Revert to the original dataset version and update UI accordingly.
        """
        original = self.window.version_manager.get_original_data()
        if original:
            self.window.data_model = original
            self.window.version_manager.update_current_data(original)
            self.window.original_button.setEnabled(False)
            self.window.missing_controller.update_data_reference(original.series)
            self.window.refresher.refresh_all(self.window, original.series)

    def update_data_versions(self):
        """
        Update dropdown menu with all available data versions.
        """
        self.window.data_version_combo.blockSignals(True)
        self.window.data_version_combo.clear()

        labels = self.window.version_manager.get_all_descriptions()
        self.window.data_version_combo.addItems(labels)

        current = self.window.version_manager.get_data_description()
        if current in labels:
            self.window.data_version_combo.setCurrentIndex(labels.index(current))

        self.window.data_version_combo.blockSignals(False)
        self._update_all()

    def update_data_version_selection(self):
        """
        Sync the dropdown selection with the currently active dataset.
        """
        labels = self.window.version_manager.get_all_descriptions()
        current = self.window.version_manager.get_data_description()

        self.window.data_version_combo.blockSignals(True)
        if current in labels:
            self.window.data_version_combo.setCurrentIndex(labels.index(current))
        self.window.data_version_combo.blockSignals(False)

        self.window.state_controller.update_navigation_buttons()

    def _update_all(self):
        """
        Internal helper to refresh UI after switching dataset.
        """
        series = self.window.data_model.series
        self.window.graph_panel.bins_spinbox.setValue(self.window.data_model.bins)
        self.window.refresher.refresh_all(self.window, series)