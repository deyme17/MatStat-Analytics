from services.transformation_service import TransformationService
from services.ui_refresh_service import UIRefreshService

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

        self.window.version_manager.update_current_data(new_model)

        UIRefreshService.refresh_all(self.window, self.window.data_model.series)
        self.window.original_button.setEnabled(True)

    def is_transformed(self):
        return len(self.window.data_model.history) > 0