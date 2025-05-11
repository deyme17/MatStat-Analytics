class DataTransformController:
    def __init__(self, window):
        self.window = window

    def standardize_data(self):
        if self.window.data is not None:
            transformed = self.window.transform_manager.standardize(self.window.data)
            self._apply_transformation(transformed)

    def log_transform_data(self):
        if self.window.data is not None:
            transformed = self.window.transform_manager.log_transform(self.window.data)
            self._apply_transformation(transformed)

    def shift_data(self):
        if self.window.data is not None:
            shift_val = self.window.shift_spinbox.value()
            transformed = self.window.transform_manager.shift(self.window.data, shift_val)
            self._apply_transformation(transformed)

    def _apply_transformation(self, data):
        self.window.data = data
        self.window.version_manager.update_current_data(data)
        self.window.version_manager.set_transform_state(
            self.window.transform_manager.get_state()
        )
        self._update_all()

    def _update_all(self):
        self.window.graph_controller.set_data(self.window.data)
        self.window.missing_controller.update_data_reference(self.window.data)
        self.window.state_controller.update_state_for_data(self.window.data)
        self.window.stat_controller.update_statistics_table()
        self.window.state_controller.update_transformation_label()
        self.window.state_controller.update_navigation_buttons()
        self.window.gof_tab.evaluate_tests()

    def is_transformed(self):
        return self.window.transform_manager.transformed_data is not None