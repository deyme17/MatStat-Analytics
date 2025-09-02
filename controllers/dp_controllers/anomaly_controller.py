from typing import Callable
import pandas as pd


class AnomalyController:
    """
    Controller for detecting and removing statistical anomalies from the dataset.
    """
    def __init__(self, context, anomaly_service, get_gamma_value):
        """    
        Args:
            context (AppContext): Application context container
            anomaly_service: Service for anomaly detection operations
            get_gamma_value: Function for getting gamma configuration
        """
        self.context = context
        self.anomaly_service = anomaly_service
        self.get_gamma_value = get_gamma_value

    def remove_sigma_anomalies(self) -> None:
        """
        Detect and remove anomalies using the standard deviation threshold method (3 sigma).
        """
        self._remove_anomalies(self.anomaly_service.detect_sigma_anomalies, "Sigma Filtered")

    def remove_asymmetry_anomalies(self) -> None:
        """
        Detect and remove anomalies based on skewness and kurtosis adjustments.
        """
        self._remove_anomalies(self.anomaly_service.detect_asymmetry_anomalies, "Asymmetry Filtered")

    def remove_conf_anomalies(self):
        """
        Detect and remove anomalies using confidence interval bounds.
        Confidence level is selected via the gamma spinbox.
        """
        gamma = self.get_gamma_value()
        func = lambda data: self.anomaly_service.detect_conf_anomalies(data, gamma)
        self._remove_anomalies(func, f"Conf. Filtered γ={gamma}")

    def _remove_anomalies(self, detection_func: Callable[[pd.Series], pd.Series], label: str) -> None:
        """
        Generic method to detect and remove anomalies using a given detection function.
        Args:
            detection_func: function that returns a dict with 'anomalies' and bounds
            label: label used to name the new version of the dataset
        """
        data = self.context.data_model.series
        if data is None:
            return

        data = data.reset_index(drop=True)
        if data.isna().sum() > 0:
            self.context.messanger.show_error("Missing Values Error", "Please handle missing values first.")
            return

        result = detection_func(data)
        anomalies = result["anomalies"]
        if len(anomalies) == 0:
            self.context.messanger.show_info("No Anomalies", "No anomalies detected.")
            return

        # Remove anomalies and create new version of the dataset
        cleaned = data.drop(anomalies)
        new_model = self.context.data_model.add_version(cleaned, label)
        new_model.anomalies_removed = True

        # Update data model and UI
        self.context.data_model = new_model
        self.context.version_manager.update_current_data(new_model)
        self.context.refresher.refresh(cleaned)

        self.context.messanger.show_info(
            "Anomalies Removed",
            f"Removed {len(anomalies)} anomalies.\n"
            f"Lower: {result['lower_limit']:.4f}, Upper: {result['upper_limit']:.4f}"
        )