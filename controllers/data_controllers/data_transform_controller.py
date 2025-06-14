from typing import Callable

class DataTransformController:
    """
    Controller for applying data transformations (standardization, log, shift).
    """
    def __init__(
        self,
        context,
        transform_service,
        shift_spinbox,
        on_transformation_applied: Callable[[], None]
    ):
        """
        Args:
            context (AppContext): Application context container
            transform_service: Service to perform data transformation
            shift_spinbox (QSpinBox): SpinBox control for data shifting
        """
        self.context = context
        self.transform_service = transform_service
        self.shift_spinbox = shift_spinbox
        self.on_transformation_applied = on_transformation_applied

    def standardize_data(self):
        """
        Apply Z-score standardization to the current dataset.
        """
        if self.context.data_model:
            transformed = self.transform_service.standardize(self.context.data_model.series)
            self._apply_transformation(transformed, "Standardized")

    def log_transform_data(self):
        """
        Apply log transformation to the current dataset, shifting if needed.
        """
        if self.context.data_model:
            transformed = self.transform_service.log_transform(self.context.data_model.series)
            self._apply_transformation(transformed, "Log Transform")

    def shift_data(self):
        """
        Apply constant shift to the current dataset based on UI input.
        """
        if self.context.data_model:
            shift_val = self.shift_spinbox.value()
            transformed = self.transform_service.shift(self.context.data_model.series, shift_val)
            self._apply_transformation(transformed, f"Shifted by {shift_val}")

    def _apply_transformation(self, new_series, label):
        """
        Internal helper to create a new DataModel version, update state and UI.

        :param new_series: transformed pandas Series
        :param label: label for the transformation version
        """
        new_model = self.context.data_model.add_version(new_series, label)
        self.context.data_model = new_model
        self.context.version_manager.update_current_data(new_model)
        self.context.refresher.refresh(self.context.data_model.series)
        
        if self.on_transformation_applied:
            self.on_transformation_applied()

    def is_transformed(self):
        """
        Check whether the current dataset has transformation history.

        :return: True if transformations applied, False otherwise
        """
        return len(self.context.data_model.history) > 0