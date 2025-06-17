from typing import Callable
from dataclasses import dataclass

@dataclass
class UIBinsControlCallbacks:
    set_enabled: Callable[[bool], None]
    set_value: Callable[[int], None]

@dataclass
class UIControlCallbacks:
    set_transform_enabled: Callable[[bool], None]
    set_anomaly_enabled: Callable[[bool], None]
    set_missing_enabled: Callable[[bool], None]
    set_transformation_label: Callable[[str], None]
    set_original_button_enabled: Callable[[bool], None]
    bins_controls: UIBinsControlCallbacks

def build_ui_control_callbacks(window) -> UIControlCallbacks:
    return UIControlCallbacks(
        set_transform_enabled=lambda val: (
            window.data_tab.standardize_button.setEnabled(val),
            window.data_tab.log_button.setEnabled(val),
            window.shift_spinbox.setEnabled(val),
            window.data_tab.shift_button.setEnabled(val)
        ),
        set_anomaly_enabled=lambda val: (
            window.data_tab.normal_anomaly_button.setEnabled(val),
            window.data_tab.asymmetry_anomaly_button.setEnabled(val),
            window.data_tab.confidence_anomaly_button.setEnabled(val),
            window.anomaly_gamma_spinbox.setEnabled(val)
        ),
        set_missing_enabled=lambda val: (
            window.data_tab.impute_mean_button.setEnabled(val),
            window.data_tab.impute_median_button.setEnabled(val),
            window.data_tab.interpolate_linear_button.setEnabled(val),
            window.data_tab.drop_missing_button.setEnabled(val)
        ),
        set_transformation_label=lambda text: window.data_tab.transformation_label.setText(text),
        set_original_button_enabled=lambda val: window.original_button.setEnabled(val),
        bins_controls=UIBinsControlCallbacks(
            set_enabled=window.graph_panel.bins_spinbox.setEnabled,
            set_value=window.graph_panel.bins_spinbox.setValue
        )
    )
