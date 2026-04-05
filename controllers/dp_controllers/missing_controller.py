from utils import AppContext, EventBus, EventType
from services import DataVersionManager, UIMessager
from models import MissingProcessor
import pandas as pd


class MissingDataController:
    """
    Controller for handling missing data operations.
    """
    def __init__(self, context: AppContext, missing_proc: MissingProcessor):
        """
        Args:
            context: Application context container
            missing_proc: Class for missing data handling
        """
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.messanger: UIMessager = context.messanger
        self.version_manager: DataVersionManager = context.version_manager
        self.missing_proc: MissingProcessor = missing_proc
        self.data: pd.Series | None = None

        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        self.event_bus.subscribe(EventType.DATA_LOADED,     self._on_data_changed)
        self.event_bus.subscribe(EventType.DATA_REVERTED,   self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.COLUMN_CHANGED,  self._on_data_changed)

    def _on_data_changed(self, event) -> None:
        series = self.context.data_model.series
        if series is not None:
            self.update_data_reference(series)

    def update_data_reference(self, data: pd.Series) -> None:
        self.data = data
        self.update_missing_values_info()

    def update_missing_values_info(self) -> None:
        if self.data is None:
            return

        info = self.missing_proc.detect_missing(self.data)
        
        self.event_bus.emit_type(EventType.MISSING_VALUES_INFO, info)
        if info['total_missing'] > 0:
            self.event_bus.emit_type(EventType.MISSING_VALUES_DETECTED)
            self.messanger.show_info(
                "Missing Values Detected",
                f"Found {info['total_missing']} missing values "
                f"({info['missing_percentage']:.2f}%).\n"
                "Please handle missing values before performing data operations."
            )
        else:
            self.event_bus.emit_type(EventType.MISSING_VALUES_HANDLED)

    def impute_with_mean(self) -> None:
        if self.data is not None:
            new_series = self.missing_proc.replace_missing_with_mean(self.data)
            self._update_after_imputation(new_series, "Mean Imputed", "Missing values replaced with mean successfully.")

    def impute_with_median(self) -> None:
        if self.data is not None:
            new_series = self.missing_proc.replace_missing_with_median(self.data)
            self._update_after_imputation(new_series, "Median Imputed", "Missing values replaced with median successfully.")

    def interpolate_missing(self, method: str) -> None:
        if self.data is not None:
            new_series = self.missing_proc.interpolate_missing(self.data, method)
            self._update_after_imputation(new_series, f"Interpolated ({method})", f"Missing values interpolated ({method}) successfully.")

    def drop_missing_values(self) -> None:
        if self.data is not None:
            original_len = len(self.data)
            new_series = self.missing_proc.drop_missing(self.data)
            dropped = original_len - len(new_series)
            self._update_after_imputation(new_series, "Dropped NA", f"Dropped {dropped} rows with missing values.")

    def _update_after_imputation(self, new_series: pd.Series, label: str, message: str) -> None:
        new_df = pd.DataFrame(new_series).reset_index(drop=True)
        new_model = self.context.data_model.add_version(new_df, label)
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