class DataVersionController:
    def __init__(self, window):
        self.window = window

    def on_data_version_changed(self, index):
        labels = self.window.version_manager.get_all_descriptions()
        if 0 <= index < len(labels):
            label = labels[index]
            self.window.version_manager.switch_to(label)
            self.window.data_model = self.window.version_manager.get_current_data()
            self._update_all()

    def original_data(self):
        original = self.window.version_manager.get_original_data()
        if original:
            self.window.data_model = original
            self.window.version_manager.update_current_data(original)
            self.window.original_button.setEnabled(False)
            self.window.missing_controller.update_data_reference(original.series)

            has_missing = original.series.isna().sum() > 0
            if has_missing:
                self.window.graph_panel.clear()
                self.window.stat_controller.clear()
                self.window.gof_tab.clear_tests()

            self._update_all()

    def update_data_versions(self):
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
        labels = self.window.version_manager.get_all_descriptions()
        current = self.window.version_manager.get_data_description()

        self.window.data_version_combo.blockSignals(True)
        if current in labels:
            self.window.data_version_combo.setCurrentIndex(labels.index(current))
        self.window.data_version_combo.blockSignals(False)

        self.window.state_controller.update_navigation_buttons()

    def _update_all(self):
        series = self.window.data_model.series
        has_missing = series.isna().sum() > 0

        self.window.state_controller.update_state_for_data(series)
        self.window.state_controller.update_transformation_label()
        self.window.state_controller.update_navigation_buttons()
        self.window.graph_panel.bins_spinbox.setValue(self.window.data_model.bins)

        if has_missing:
            self.window.graph_panel.clear()
            self.window.graph_panel.data = None
            self.window.stat_controller.clear()
            self.window.gof_tab.clear_tests()
        else:
            self.window.graph_controller.set_data(series)
            self.window.stat_controller.update_statistics_table()
            self.window.gof_tab.evaluate_tests()