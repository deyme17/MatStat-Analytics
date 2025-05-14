from services.missing_service import MissingService
from models.data_model import DataModel
from services.ui_refresh_service import UIRefreshService

class MissingDataController:
    def __init__(self, window):
        self.window = window
        self.data = None

    def update_data_reference(self, data):
        self.data = data
        self.update_missing_values_info()
        self.window.state_controller.update_state_for_data(data)

    def update_missing_values_info(self):
        if self.data is not None:
            info = MissingService.detect_missing(self.data)
            self.window.missing_count_label.setText(f"Total Missing: {info['total_missing']}")
            self.window.missing_percentage_label.setText(f"Missing Percentage: {info['missing_percentage']:.2f}%")

    def _update_after_imputation(self, new_series, label, message):
        new_model = self.window.data_model.add_version(new_series, label)
        self.window.data_model = new_model
        self.data = new_model.series

        # save
        self.window.version_manager.update_current_data(new_model)

        UIRefreshService.refresh_all(self.window, new_series)
        self.update_missing_values_info()
        self.window.show_info_message("Success", message)


    def impute_with_mean(self):
        if self.data is not None:
            new_series = MissingService.replace_missing_with_mean(self.data)
            self._update_after_imputation(new_series, "Mean Imputed", "Missing values replaced with mean successfully.")

    def impute_with_median(self):
        if self.data is not None:
            new_series = MissingService.replace_missing_with_median(self.data)
            self._update_after_imputation(new_series, "Median Imputed", "Missing values replaced with median successfully.")

    def interpolate_missing(self, method):
        if self.data is not None:
            new_series = MissingService.interpolate_missing(self.data, method)
            self._update_after_imputation(new_series, f"Interpolated ({method})", f"Missing values interpolated ({method}) successfully.")

    def drop_missing_values(self):
        if self.data is not None:
            original_len = len(self.data)
            new_series = MissingService.drop_missing(self.data)
            dropped = original_len - len(new_series)
            self._update_after_imputation(new_series, "Dropped NA", f"Dropped {dropped} rows with missing values.")