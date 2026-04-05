from utils import AppContext, EventBus, EventType
from services import DataVersionManager
from models import TransformationProcessor
import pandas as pd


class DataTransformController:
    """
    Controller for applying data transformations (standardization, log, shift).
    """
    def __init__(self, context: AppContext, transform_proc: TransformationProcessor):
        """
        Args:
            context: Application context container
            transform_proc: Class to perform data transformation
        """
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.version_manager: DataVersionManager = context.version_manager
        self.transform_proc: TransformationProcessor = transform_proc
        self._std_params: dict[str, dict] = {}  # store params per dataset

    @property
    def std_params(self) -> dict | None:
        """Return params for current dataset, or None if not normalized."""
        name = self.version_manager.get_current_dataset_name()
        return self._std_params.get(name)

    def _save_std_params(self, params: dict) -> None:
        name = self.version_manager.get_current_dataset_name()
        self._std_params[name] = params

    def _clear_std_params(self) -> None:
        name = self.version_manager.get_current_dataset_name()
        self._std_params.pop(name, None)

    # ── transformation methods ──────────────────────────────────────────────────
    def standardize_data(self, columns: list[str] | None = None) -> None:
        """
        Standardize selected columns or current series.
        Args:
            columns: column names to standardize, or None for current series
        """
        model = self.context.data_model
        if not model:
            return

        if columns:
            transformed, params = self.transform_proc.standardize(model.dataframe[columns])
            new_df = model.dataframe.copy()
            new_df[columns] = transformed
            label = f"Standardized ({', '.join(columns)})"
            model.add_version(new_df, label)
        else:
            transformed, params = self.transform_proc.standardize(model.series)
            label = "Standardized"
            model.add_version_from_series(transformed, label)

        self._save_std_params(params)
        self._emit(label, model)

    def unstandardize_data(self) -> None:
        """Reverse standardization using stored params for current dataset."""
        model = self.context.data_model
        params = self.std_params
        if not model or not params:
            return

        label = "Unstandardized"

        if 'mean' not in params:
            # {col: (mean, std)}
            new_df = self.transform_proc.unstandardize(model.dataframe, params)
            model.add_version(new_df, label)
        else:
            # {'mean': float, 'std': float}
            restored = self.transform_proc.unstandardize(model.series, params)
            model.add_version_from_series(restored, label)

        self._clear_std_params()
        self._emit(label, model)

    def log_transform_data(self, kind: str = "ln") -> None:
        if self.context.data_model:
            transformed = self.transform_proc.log_transform(self.context.data_model.series, kind=kind)
            self._apply_series(transformed, f"Log Transform ({kind})")

    def inverse_log_transform_data(self, kind: str = "ln") -> None:
        if self.context.data_model:
            transformed = self.transform_proc.inverse_log_transform(self.context.data_model.series, kind=kind)
            self._apply_series(transformed, f"Inv. Log ({kind})")

    def shift_data(self, shift_value: float) -> None:
        if self.context.data_model:
            transformed = self.transform_proc.shift(self.context.data_model.series, shift_value)
            self._apply_series(transformed, f"Shifted by {shift_value}")

    # ── internal ──────────────────────────────────────────────────
    def _apply_series(self, new_series: pd.Series, label: str) -> None:
        model = self.context.data_model
        model.add_version_from_series(new_series, label)
        self.version_manager.update_current_dataset(model)
        self._emit(label, model)

    def _emit(self, label: str, model) -> None:
        self.event_bus.emit_type(EventType.DATA_TRANSFORMED, {
            'model': model,
            'series': model.series,
            'label': label
        })