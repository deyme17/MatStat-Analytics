from typing import Optional
from services import MissingInfoDisplayService, MissingService, DataVersionManager, UIMessager
from models.data_model import DataModel
from utils import AppContext, EventBus, EventType
import pandas as pd


class MissingDataController:
    """
    Controller for handling missing data operations.
    """
    def __init__(
        self,
        context: AppContext,
        missing_service,
        display_service: Optional[MissingInfoDisplayService] = None
    ):
        """
        Args:
            context: Application context container
            missing_service: Service for missing data handling
            display_service: Service for displaying missing data info
        """
        self.context: AppContext = context
        self.data_model: DataModel = context.data_model
        self.event_bus: EventBus = context.event_bus
        self.messanger: UIMessager = context.messanger
        self.version_manager: DataVersionManager = context.version_manager
        self.missing_service: MissingService = missing_service
        self.display_service: MissingInfoDisplayService = display_service
        self.data = None
        
        self._subscribe_to_events()

    def _subscribe_to_events(self):
        self.event_bus.subscribe(EventType.DATA_LOADED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATA_REVERTED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.COLUMN_CHANGED, self._on_data_changed)

    def _on_data_changed(self, event):
        series = event.data.get('series')
        if series is not None:
            self.update_data_reference(series)

    def update_data_reference(self, data: pd.Series) -> None:
        """
        Update the internal data reference and refresh missing values info.
        Args:
            data: New data series to reference
        """
        self.data = data
        self.update_missing_values_info()

    def update_missing_values_info(self) -> None:
        """
        Update the display with current missing values information.
        """
        if not self.display_service:
            return
        if self.data is not None:
            info = self.missing_service.detect_missing(self.data)
            self.display_service.update(info)
            
            if info['count'] > 0:
                self.event_bus.emit_type(EventType.MISSING_VALUES_DETECTED, info)

    def impute_with_mean(self) -> None:
        """
        Replace missing values with the mean of the series.
        """
        if self.data is not None:
            new_series = self.missing_service.replace_missing_with_mean(self.data)
            self._update_after_imputation(new_series, "Mean Imputed", "Missing values replaced with mean successfully.")

    def impute_with_median(self) -> None:
        """
        Replace missing values with the median of the series.
        """
        if self.data is not None:
            new_series = self.missing_service.replace_missing_with_median(self.data)
            self._update_after_imputation(new_series, "Median Imputed", "Missing values replaced with median successfully.")

    def interpolate_missing(self, method: str) -> None:
        """
        Interpolate missing values using specified method.
        Args:
            method: Interpolation method to use
        """
        if self.data is not None:
            new_series = self.missing_service.interpolate_missing(self.data, method)
            self._update_after_imputation(new_series, f"Interpolated ({method})", f"Missing values interpolated ({method}) successfully.")

    def drop_missing_values(self) -> None:
        """
        Drop rows containing missing values from the series.
        """
        if self.data is not None:
            original_len = len(self.data)
            new_series = self.missing_service.drop_missing(self.data)
            dropped = original_len - len(new_series)
            self._update_after_imputation(new_series, "Dropped NA", f"Dropped {dropped} rows with missing values.")

    def _update_after_imputation(self, new_series: pd.Series, label: str, message: str) -> None:
        """
        Internal helper to update state after missing data imputation.
        Args:
            new_series: Transformed pandas Series
            label: Label for the transformation version
            message: Success message to display
        """
        new_df = pd.DataFrame(new_series).reset_index(drop=True)

        new_model = self.data_model.add_version(new_df, label)
        self.context.data_model = new_model
        self.data = new_model.series

        self.version_manager.update_current_dataset(new_model)
        
        self.event_bus.emit_type(EventType.MISSING_VALUES_HANDLED)
        self.event_bus.emit_type(EventType.DATA_TRANSFORMED, {
            'model': new_model,
            'series': new_model.series,
            'label': label
        })
        self.update_missing_values_info()
        self.messanger.show_info("Success", message)

    def connect_ui(self, display_service: MissingInfoDisplayService) -> None:
        self.display_service = display_service