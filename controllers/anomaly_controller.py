from services.anomaly_service import AnomalyService
from models.data_model import DataModel
from services.ui_refresh_service import UIRefreshService

class AnomalyController:
    def __init__(self, window):
        self.window = window

    def remove_normal_anomalies(self):
        self._remove_anomalies(AnomalyService.detect_normal_anomalies, "Normal Filtered")

    def remove_asymmetry_anomalies(self):
        self._remove_anomalies(AnomalyService.detect_asymmetry_anomalies, "Asymmetry Filtered")

    def remove_conf_anomalies(self):
        gamma = self.window.anomaly_gamma_spinbox.value()
        func = lambda data: AnomalyService.detect_conf_anomalies(data, gamma)
        self._remove_anomalies(func, f"Conf. Filtered γ={gamma}")

    def _remove_anomalies(self, detection_func, label):
        data = self.window.data_model.series
        if data is None:
            return

        data = data.reset_index(drop=True)
        if data.isna().sum() > 0:
            self.window.show_error_message("Missing Values Error", "Please handle missing values first.")
            return

        result = detection_func(data)
        anomalies = result["anomalies"]
        if len(anomalies) == 0:
            self.window.show_info_message("No Anomalies", "No anomalies detected.")
            return

        cleaned = data.drop(anomalies)
        new_model = self.window.data_model.add_version(cleaned, label)
        new_model.anomalies_removed = True

        self.window.data_model = new_model

        # save
        self.window.version_manager.update_current_data(new_model)
        UIRefreshService.refresh_all(self.window, cleaned)

        self.window.show_info_message(
            "Anomalies Removed",
            f"Removed {len(anomalies)} anomalies.\n"
            f"Lower: {result['lower_limit']:.4f}, Upper: {result['upper_limit']:.4f}"
        )
