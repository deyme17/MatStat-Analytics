from utils import AppContext, EventBus, EventType
from services import DataVersionManager
from models import TransformationProcessor
from typing import Callable, Optional
import pandas as pd


class DataTransformController:
    """
    Controller for applying data transformations (standardization, log, shift).
    """
    def __init__(
        self,
        context: AppContext,
        transform_proc: TransformationProcessor,
        get_shift_value: Optional[Callable[[], int]] = None
    ):
        """
        Args:
            context: Application context container
            transform_proc: Class to perform data transformation
            get_shift_value: Function for getting shift configuration
        """
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.version_manager: DataVersionManager = context.version_manager
        self.transform_proc: TransformationProcessor = transform_proc
        self.get_shift_value = get_shift_value

    def standardize_data(self) -> None:
        """
        Apply Z-score standardization to the current dataset.
        """
        if self.context.data_model:
            transformed = self.transform_proc.standardize(self.context.data_model.series)
            self._apply_transformation(transformed, "Standardized")

    def log_transform_data(self) -> None:
        """
        Apply log transformation to the current dataset, shifting if needed.
        """
        if self.context.data_model:
            transformed = self.transform_proc.log_transform(self.context.data_model.series)
            self._apply_transformation(transformed, "Log Transform")

    def shift_data(self) -> None:
        """
        Apply constant shift to the current dataset based on UI input.
        """
        if not self.get_shift_value:
            raise RuntimeError("No get_shift_value function provided in DataTransformController")
        if self.context.data_model:
            shift_val = self.get_shift_value()
            transformed = self.transform_proc.shift(self.context.data_model.series, shift_val)
            self._apply_transformation(transformed, f"Shifted by {shift_val}")

    def _apply_transformation(self, new_series: pd.Series, label: str) -> None:
        """
        Internal helper to create a new DataModel version, update state and UI.
        Args:
            new_series: transformed pandas Series
            label: label for the transformation version
        """
        new_model = self.context.data_model.add_version_from_series(new_series, label)
        self.context.data_model = new_model
        self.version_manager.update_current_dataset(new_model)
        
        self.event_bus.emit_type(EventType.DATA_TRANSFORMED, {
            'model': new_model,
            'series': new_model.series,
            'label': label
        })

    def is_transformed(self) -> bool:
        """
        Check whether the current dataset has transformation history.
        Return:
            True if transformations applied, False otherwise
        """
        return len(self.context.data_model.history) > 0
    
    def connect_ui(self, get_shift_value: Callable[[], int]) -> None:
        self.get_shift_value = get_shift_value