from typing import Callable, Optional
import pandas as pd

from utils import AppContext, EventBus, EventType
from utils.decorators import require_one_dimensional_dataframe
from services import DataVersionManager, UIMessager
from models import AnomalyProcessor


class AnomalyController:
    """
    Controller for detecting and removing statistical anomalies from the dataset.
    """
    def __init__(
        self, 
        context: AppContext, 
        anomaly_proc: AnomalyProcessor, 
        get_gamma_value: Optional[Callable[[], float]] = None
    ):
        """    
        Args:
            context: Application context container
            anomaly_proc: Class for anomaly detection operations
            get_gamma_value: Function for getting gamma configuration
        """
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.version_manager: DataVersionManager = context.version_manager
        self.messanger: UIMessager = context.messanger
        self.anomaly_proc: AnomalyProcessor = anomaly_proc
        self.get_gamma_value = get_gamma_value

    @require_one_dimensional_dataframe
    def remove_sigma_anomalies(self, *args, **kwargs) -> None:
        """
        Detect and remove anomalies using the standard deviation threshold method (3 sigma).
        """
        self._remove_anomalies(self.anomaly_proc.detect_sigma_anomalies, "Sigma Filtered")

    @require_one_dimensional_dataframe
    def remove_asymmetry_anomalies(self, *args, **kwargs) -> None:
        """
        Detect and remove anomalies based on skewness and kurtosis adjustments.
        """
        self._remove_anomalies(self.anomaly_proc.detect_asymmetry_anomalies, "Asymmetry Filtered")

    @require_one_dimensional_dataframe
    def remove_conf_anomalies(self, *args, **kwargs):
        """
        Detect and remove anomalies using confidence interval bounds.
        Confidence level is selected via the gamma spinbox.
        """
        if not self.get_gamma_value:
            raise RuntimeError("No get_gamma_value function provided in AnomalyController")
        gamma = self.get_gamma_value()
        func = lambda data: self.anomaly_proc.detect_conf_anomalies(data, gamma)
        self._remove_anomalies(func, f"Conf. Filtered γ={gamma}")

    def _remove_anomalies(self, detection_func: Callable[[pd.DataFrame], pd.DataFrame], label: str) -> None:
        """
        Generic method to detect and remove anomalies using a given detection function.
        Args:
            detection_func: function that returns a dict with 'anomalies' and bounds
            label: label used to name the new version of the dataset
        """
        data = self.context.data_model.dataframe
        if data is None:
            return

        data = data.reset_index(drop=True)
        if data.isna().sum().iloc[0] > 0:
            self.messanger.show_error("Missing Values Error", "Please handle missing values first.")
            return

        result = detection_func(data)
        anomalies = result["anomalies"]
        if len(anomalies) == 0:
            self.messanger.show_info("No Anomalies", "No anomalies detected.")
            return

        # remove anomalies and create new version of the dataset
        cleaned = data.drop(anomalies)
        new_model = self.context.data_model.add_version(cleaned, label)
        new_model.anomalies_removed = True
        current_col = new_model.current_col_idx

        # update data model and UI
        self.context.data_model = new_model
        self.version_manager.update_current_dataset(new_model)
        
        self.event_bus.emit_type(EventType.DATA_TRANSFORMED, {
            'model': new_model,
            'series': cleaned.iloc[:, current_col],
            'label': label,
            'anomalies_count': len(anomalies),
            'bounds': {
                'lower': result['lower_limit'],
                'upper': result['upper_limit']
            }
        })
        self.messanger.show_info(
            "Anomalies Removed",
            f"Removed {len(anomalies)} anomalies.\n"
            f"Lower: {result['lower_limit']:.4f}, Upper: {result['upper_limit']:.4f}"
        )

    def connect_ui(self, get_gamma_value: Callable[[], float]) -> None:
        self.get_gamma_value = get_gamma_value