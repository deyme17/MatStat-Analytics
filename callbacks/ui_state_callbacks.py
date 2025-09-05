from typing import Callable
from dataclasses import dataclass

@dataclass
class UIBinsControlCallbacks:
    set_enabled: Callable[[bool], None]
    set_value: Callable[[int], None]

@dataclass
class DPControlCallbacks:
    set_transform_enabled: Callable[[bool], None]
    set_anomaly_enabled: Callable[[bool], None]
    set_missing_enabled: Callable[[bool], None]
    set_transformation_label: Callable[[str], None]
    set_original_button_enabled: Callable[[bool], None]
    bins_controls: UIBinsControlCallbacks

def build_dp_control_callbacks(window) -> DPControlCallbacks:
    data_tab = window.left_tab_widget.data_tab
    return DPControlCallbacks(
        set_transform_enabled=lambda val: (
            data_tab.transform_widget.standardize_button.setEnabled(val),
            data_tab.transform_widget.log_button.setEnabled(val),
            data_tab.transform_widget.shift_spinbox.setEnabled(val),
            data_tab.transform_widget.shift_button.setEnabled(val)
        ),
        set_anomaly_enabled=lambda val: (
            data_tab.anomaly_widget.sigma_anomaly_button.setEnabled(val),
            data_tab.anomaly_widget.asymmetry_anomaly_button.setEnabled(val),
            data_tab.anomaly_widget.confidence_anomaly_button.setEnabled(val),
            data_tab.anomaly_widget.anomaly_gamma_spinbox.setEnabled(val)
        ),
        set_missing_enabled=lambda val: (
            data_tab.missing_widget.impute_mean_button.setEnabled(val),
            data_tab.missing_widget.impute_median_button.setEnabled(val),
            data_tab.missing_widget.interpolate_linear_button.setEnabled(val),
            data_tab.missing_widget.drop_missing_button.setEnabled(val)
        ),
        set_transformation_label=lambda text: data_tab.transformation_label.setText(text),
        set_original_button_enabled=lambda val: data_tab.original_button.setEnabled(val),
        bins_controls=UIBinsControlCallbacks(
            set_enabled=window.graph_panel.bins_spinbox.setEnabled,
            set_value=window.graph_panel.bins_spinbox.setValue
        )
    )
