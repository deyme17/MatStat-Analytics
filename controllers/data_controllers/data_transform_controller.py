from services.data_services.transformation_service import TransformationService
from services.ui_services.ui_refresh_service import UIRefreshService

class DataTransformController:
    """
    Controller for applying data transformations (standardization, log, shift).
    """

    def __init__(self, window):
        self.window = window

    def standardize_data(self):
        """
        Apply Z-score standardization to the current dataset.
        """
        if self.window.data_model:
            transformed = TransformationService.standardize(self.window.data_model.series)
            self._apply_transformation(transformed, "Standardized")

    def log_transform_data(self):
        """
        Apply log transformation to the current dataset, shifting if needed.
        """
        if self.window.data_model:
            transformed = TransformationService.log_transform(self.window.data_model.series)
            self._apply_transformation(transformed, "Log Transform")

    def shift_data(self):
        """
        Apply constant shift to the current dataset based on UI input.
        """
        if self.window.data_model:
            shift_val = self.window.shift_spinbox.value()
            transformed = TransformationService.shift(self.window.data_model.series, shift_val)
            self._apply_transformation(transformed, f"Shifted by {shift_val}")

    def _apply_transformation(self, new_series, label):
        """
        Internal helper to create a new DataModel version, update state and UI.

        :param new_series: transformed pandas Series
        :param label: label for the transformation version
        """
        new_model = self.window.data_model.add_version(new_series, label)
        self.window.data_model = new_model
        self.window.version_manager.update_current_data(new_model)
        UIRefreshService.refresh_all(self.window, self.window.data_model.series)
        self.window.original_button.setEnabled(True)

    def is_transformed(self):
        """
        Check whether the current dataset has transformation history.

        :return: True if transformations applied, False otherwise
        """
        return len(self.window.data_model.history) > 0