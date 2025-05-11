class DataVersionController:
    def __init__(self, window):
        self.window = window

    def on_data_version_changed(self, index):
        if 0 <= index < len(self.window.version_manager.data_history):
            self.window.version_manager.current_index = index
            self.window.transform_manager.reset()
            self.window.data = self.window.version_manager.get_current_data()
            transform_state = self.window.version_manager.get_transform_state()
            self.window.transform_manager.load_state(transform_state)
            self._update_all()

    def original_data(self):
        self.window.transform_manager.reset()
        restored = self.window.version_manager.get_original_data()
        self.window.data = restored
        self.window.version_manager.update_current_data(restored)
        self.window.anomalies_removed = False
        self.window.original_button.setEnabled(False)
        self._update_all()

    def update_data_versions(self):
        self.window.data_version_combo.blockSignals(True)
        self.window.data_version_combo.clear()
        descriptions = self.window.version_manager.get_all_descriptions()
        self.window.data_version_combo.addItems(descriptions)
        self.window.data_version_combo.setCurrentIndex(self.window.version_manager.current_index)
        self.window.data_version_combo.blockSignals(False)
        self._update_all()

    def update_data_version_selection(self):
        self.window.data_version_combo.blockSignals(True)
        self.window.data_version_combo.setCurrentIndex(self.window.version_manager.current_index)
        self.window.data_version_combo.blockSignals(False)
        self.window.state_controller.update_navigation_buttons()

    def _update_all(self):
        self.window.graph_controller.set_data(self.window.data)
        self.window.missing_controller.update_data_reference(self.window.data)
        self.window.stat_controller.update_statistics_table()
        self.window.gof_tab.evaluate_tests()
        self.window.state_controller.update_state_for_data(self.window.data)
        self.window.state_controller.update_transformation_label()
        self.window.state_controller.update_navigation_buttons()