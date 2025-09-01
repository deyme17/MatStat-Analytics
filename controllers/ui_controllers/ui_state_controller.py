import pandas as pd
from typing import Callable


class UIStateController:
    """
    Controller responsible for enabling/disabling UI elements based on data state.
    """
    def __init__(
        self,
        context,
        missing_service,
        data_version_combo,
        ui_controls,
        update_data_callback: Callable[[pd.Series], None]
    ):
        """
        Initializes the UI state controller.
        Args:
            context: Main application context with services and models
            missing_service: Handles missing data operations
            data_version_combo: Dropdown widget for dataset versions
            ui_controls: Container of UI control callbacks
            update_data_callback: Callback to update data reference in other controllers
        """
        self.context = context
        self.missing_service = missing_service
        self.data_version_combo = data_version_combo
        self.ui = ui_controls
        self.update_data_callback = update_data_callback

    def handle_post_load_state(self, data: pd.Series) -> None:
        """
        Updates UI state and handles missing values and control logic after data load.
        """
        missing_info = self.missing_service.detect_missing(data)
        has_missing = missing_info['total_missing'] > 0

        self.ui.bins_controls.set_enabled(True)
        self.data_version_combo.setEnabled(True)

        self.update_state_for_data(data)
        self.context.data_version_controller.update_data_versions()
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
        text = self.context.data_model.current_transformation if self.context.data_model else "Original"
        self.ui.set_transformation_label(f"Current state: {text}")

    def update_navigation_buttons(self) -> None:
        """
        Enables/disables navigation buttons based on transformation history.
        """
        model = self.context.data_model
        has_history = model and len(model.history) > 0
        was_anomaly_removed = getattr(model, 'anomalies_removed', False)

        self.ui.set_original_button_enabled(has_history or was_anomaly_removed)