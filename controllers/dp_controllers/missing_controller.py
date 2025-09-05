from typing import Callable, Optional
from services import MissingInfoDisplayService
import pandas as pd


class MissingDataController:
    """
    Controller for handling missing data operations.
    """
    def __init__(
        self,
        context,
        missing_service,
        display_service: Optional[MissingInfoDisplayService] = None,
        update_state_callback: Optional[Callable[[pd.Series], None]] = None
    ):
        """
        Args:
            context (AppContext): Application context container
            missing_service: Service for missing data handling
            display_service: Service for displaying missing data info
            update_state_callback (Callable): Function to call when data state changes
        """
        self.context = context
        self.missing_service = missing_service
        self.display_service = display_service
        self.update_state_callback = update_state_callback
        self.data = None

    def update_data_reference(self, data: pd.Series) -> None:
        """
        Update the internal data reference and refresh missing values info.
        Args:
            data (pd.Series): New data series to reference
        """
        if not self.update_state_callback: raise RuntimeError("No update_state_callback provided in MissingDataController")
        self.data = data
        self.update_missing_values_info()
        self.update_state_callback(data)

    def update_missing_values_info(self) -> None:
        """
        Update the display with current missing values information.
        """
        if not self.display_service: raise RuntimeError("No display_service provided in MissingDataController")
        if self.data is not None:
            info = self.missing_service.detect_missing(self.data)
            self.display_service.update(info)

    def _update_after_imputation(self, new_series: pd.Series, label: str, message: str) -> None:
        """
        Internal helper to update state after missing data imputation.
        Args:
            new_series (pd.Series): Transformed pandas Series
            label (str): Label for the transformation version
            message (str): Success message to display
        """
        new_model = self.context.data_model.add_version(new_series, label)
        self.context.data_model = new_model
        self.data = new_model.series

        self.context.version_manager.update_current_data(new_model)
        self.context.refresher.refresh(new_series)
        self.update_missing_values_info()
        self.context.messanger.show_info("Success", message)

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
            method (str): Interpolation method to use
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

    def set_display_service(self, display_service: MissingInfoDisplayService) -> None:
        self.display_service = display_service
    def set_update_state_callback(self, update_state_callback: Callable[[pd.Series], None]) -> None:
        self.update_state_callback = update_state_callback