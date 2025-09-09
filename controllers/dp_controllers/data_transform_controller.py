from typing import Callable, Optional
import pandas as pd


class DataTransformController:
    """
    Controller for applying data transformations (standardization, log, shift).
    """
    def __init__(
        self,
        context,
        transform_service,
        get_shift_value: Optional[Callable[[], int]] = None,
        on_transformation_applied: Optional[Callable[[], None]] = None
    ):
        """
        Args:
            context (AppContext): Application context container
            transform_service: Service to perform data transformation
            get_shift_value: Function for getting shift configuration
            on_transformation_applied: Callback after applying any transformation
        """
        self.context = context
        self.transform_service = transform_service
        self.get_shift_value = get_shift_value
        self.on_transformation_applied = on_transformation_applied

    def standardize_data(self) -> None:
        """
        Apply Z-score standardization to the current dataset.
        """
        if self.context.data_model:
            transformed = self.transform_service.standardize(self.context.data_model.series)
            self._apply_transformation(transformed, "Standardized")

    def log_transform_data(self) -> None:
        """
        Apply log transformation to the current dataset, shifting if needed.
        """
        if self.context.data_model:
            transformed = self.transform_service.log_transform(self.context.data_model.series)
            self._apply_transformation(transformed, "Log Transform")

    def shift_data(self) -> None:
        """
        Apply constant shift to the current dataset based on UI input.
        """
        if not self.get_shift_value: raise RuntimeError("No get_shift_value function provided in DataTransformController")
        if self.context.data_model:
            shift_val = self.get_shift_value()
            transformed = self.transform_service.shift(self.context.data_model.series, shift_val)
            self._apply_transformation(transformed, f"Shifted by {shift_val}")

    def _apply_transformation(self, new_series: pd.Series, label: str) -> None:
        """
        Internal helper to create a new DataModel version, update state and UI.
        Args:
            new_series: transformed pandas Series
            label: label for the transformation version
        """
        if not self.on_transformation_applied: raise RuntimeError("No on_transformation_applied callback provided in DataTransformController")
        new_model = self.context.data_model.add_version_from_series(new_series, label)
        self.context.data_model = new_model
        self.context.version_manager.update_current_dataset(new_model)
        self.context.refresher.refresh(self.context.data_model.series)
        self.on_transformation_applied()

    def is_transformed(self) -> bool:
        """
        Check whether the current dataset has transformation history.
        Return:
            True if transformations applied, False otherwise
        """
        return len(self.context.data_model.history) > 0
    
    def set_get_shift_value_func(self, get_shift_value: Callable[[], int]) -> None:
        self.get_shift_value = get_shift_value
    def set_on_transformation_applied_callback(self, on_transformation_applied: Callable[[], None]) -> None:
        self.on_transformation_applied = on_transformation_applied