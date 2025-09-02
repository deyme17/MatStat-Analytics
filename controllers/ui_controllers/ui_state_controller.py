import pandas as pd
from typing import Callable, Any, Optional
from callbacks.ui_state_callbacks import DPControlCallbacks


class UIStateController:
    """
    Controller responsible for enabling/disabling UI elements based on data state.
    """
    def __init__(
        self,
        context,
        ui_controls: Optional[DPControlCallbacks],
        detect_missing_func: Callable[[pd.Series], dict[str, Any]],
        enable_data_combo_callback: Optional[Callable[[bool], None]],
        update_data_callback: Optional[Callable[[pd.Series], None]],
        update_data_versions_callback: Optional[Callable[[], None]]
    ):
        """
        Initializes the UI state controller.
        Args:
            context: Main application context with services and models
            detect_missing_func: Function for detect missing data and get info
            ui_controls: Container of UI control callbacks
            enable_data_combo_callback: Callback to unable data version combo
            update_data_callback: Callback to update data reference in other controllers
            update_data_versions_callback: Callback to update dropdown menu with all available data versions.
        """
        self.context = context
        self.ui = ui_controls
        self.detect_missing_func = detect_missing_func
        self.enable_data_combo_callback = enable_data_combo_callback
        self.update_data_callback = update_data_callback
        self.update_data_versions_callback = update_data_versions_callback

    def handle_post_load_state(self, data: pd.Series) -> None:
        """
        Updates UI state and handles missing values and control logic after data load.
        """
        self.check_all_callbacks()
        missing_info = self.detect_missing_func(data)
        has_missing = missing_info['total_missing'] > 0

        self.ui.bins_controls.set_enabled(True)
        self.enable_data_combo_callback(True)

        self.update_state_for_data(data)
        self.update_data_versions_callback()
        self.update_data_callback(data)  

        self.ui.bins_controls.set_value(self.context.data_model.bins)

        if has_missing:
            self.context.messanger.show_info(
                "Missing Values Detected",
                f"Found {missing_info['total_missing']} missing values "
                f"({missing_info['missing_percentage']:.2f}%).\n"
                "Please handle missing values before performing data operations."
            )
            self.context.refresher.clear_ui()
        else:
            self.context.refresher.refresh(self.context.data_model.series)

    def update_state_for_data(self, data: pd.Series) -> None:
        """
        Enables/disables UI controls based on the presence of missing values.
        """
        self.check_all_callbacks()
        has_missing = data.isna().sum() > 0 if hasattr(data, 'isna') else False

        self.ui.set_transform_enabled(not has_missing)
        self.ui.set_anomaly_enabled(not has_missing)
        self.ui.set_missing_enabled(has_missing)

        self.update_transformation_label()
        self.update_navigation_buttons()

    def update_transformation_label(self) -> None:
        """
        Updates the UI label showing the current transformation state.
        """
        self.check_all_callbacks()
        text = self.context.data_model.current_transformation if self.context.data_model else "Original"
        self.ui.set_transformation_label(f"Current state: {text}")

    def update_navigation_buttons(self) -> None:
        """
        Enables/disables navigation buttons based on transformation history.
        """
        self.check_all_callbacks()
        model = self.context.data_model
        has_history = model and len(model.history) > 0
        was_anomaly_removed = getattr(model, 'anomalies_removed', False)

        self.ui.set_original_button_enabled(has_history or was_anomaly_removed)

    def connect_callbacks(self, ui_controls: DPControlCallbacks,
                                enable_data_combo_callback: Callable[[bool], None],
                                update_data_callback: Callable[[pd.Series], None],
                                update_data_versions_callback: Callable[[], None]) -> None:
        self.ui = ui_controls
        self.enable_data_combo_callback = enable_data_combo_callback
        self.update_data_callback = update_data_callback
        self.update_data_versions_callback = update_data_versions_callback

    def check_all_callbacks(self) -> None:
        if not (self.ui and self.enable_data_combo_callback and 
                self.update_data_callback and self.update_data_versions_callback):
            raise RuntimeError("Not all callbacks provided for UIStateController")