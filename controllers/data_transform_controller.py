from services.transformation_service import TransformationService

class DataTransformController:
    def __init__(self, window):
        self.window = window

    def standardize_data(self):
        if self.window.data_model:
            transformed = TransformationService.standardize(self.window.data_model.series)
            self._apply_transformation(transformed, "Standardized")

    def log_transform_data(self):
        if self.window.data_model:
            transformed = TransformationService.log_transform(self.window.data_model.series)
            self._apply_transformation(transformed, "Log Transform")

    def shift_data(self):
        if self.window.data_model:
            shift_val = self.window.shift_spinbox.value()
            transformed = TransformationService.shift(self.window.data_model.series, shift_val)
            self._apply_transformation(transformed, f"Shifted by {shift_val}")

    def _apply_transformation(self, new_series, label):
        new_model = self.window.data_model.add_version(new_series, label)
        self.window.data_model = new_model

        # 🔁 Зберегти в менеджері
        self.window.version_manager.update_current_data(new_model)

        self._update_all()
        self.window.original_button.setEnabled(True)

    def _update_all(self):
        self.window.graph_controller.set_data(self.window.data_model.series)
        self.window.missing_controller.update_data_reference(self.window.data_model.series)
        self.window.state_controller.update_state_for_data(self.window.data_model.series)
        self.window.stat_controller.update_statistics_table()
        self.window.state_controller.update_transformation_label()
        self.window.state_controller.update_navigation_buttons()
        self.window.gof_tab.evaluate_tests()

    def is_transformed(self):
        return len(self.window.data_model.history) > 0