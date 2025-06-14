from typing import Callable
import pandas as pd


class UIStateController:
    """
    Controller responsible for enabling/disabling UI elements based on data state.
    """
    def __init__(
        self,
        context,
        missing_service,
        data_version_combo,
        set_transform_enabled: Callable[[bool], None],
        set_anomaly_enabled: Callable[[bool], None],
        set_missing_enabled: Callable[[bool], None],
        set_transformation_label: Callable[[str], None],
        set_original_button_enabled: Callable[[bool], None]
    ):
        """
        :param context: Shared AppContext with data and services
        :param missing_service: Service for detecting missing values
        :param data_version_combo: Dataset version dropdown
        :param set_transform_enabled: Enable/disable transform controls
        :param set_anomaly_enabled: Enable/disable anomaly controls
        :param set_missing_enabled: Enable/disable missing controls
        :param set_transformation_label: Set current transformation label
        :param set_original_button_enabled: Enable/disable original revert button
        """
        self.context = context
        self.missing_service = missing_service
        self.data_version_combo = data_version_combo

        self.set_transform_enabled = set_transform_enabled
        self.set_anomaly_enabled = set_anomaly_enabled
        self.set_missing_enabled = set_missing_enabled
        self.set_transformation_label = set_transformation_label
        self.set_original_button_enabled = set_original_button_enabled

    def handle_post_load_state(self, data: pd.Series) -> None:
        """
        Updates UI state and handles missing values and control logic after data load.
        """
        missing_info = self.missing_service.detect_missing(data)
        has_missing = missing_info['total_missing'] > 0

        # Enable basic controls
        self.context.bins_spinbox.setEnabled(True)
        self.data_version_combo.setEnabled(True)

        # Update controls
        self.update_state_for_data(data)

        # Update additional state (like versions, missing stats)
        self.context.data_version_controller.update_data_versions()
        self.context.missing_controller.update_data_reference(data)

        # Set current bin count
        bin_count = self.context.data_model.bins
        self.context.bins_spinbox.setValue(bin_count)

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
        Updates UI state depending on whether the data has missing values.
        """
        has_missing = data.isna().sum() > 0 if hasattr(data, 'isna') else False

        self.set_transform_enabled(not has_missing)
        self.set_anomaly_enabled(not has_missing)
        self.set_missing_enabled(has_missing)

        self.update_transformation_label()
        self.update_navigation_buttons()

    def update_transformation_label(self) -> None:
        """
        Update label showing the current data transformation.
        """
        text = self.context.data_model.current_transformation if self.context.data_model else "Original"
        self.set_transformation_label(f"Current state: {text}")

    def update_navigation_buttons(self) -> None:
        """
        Enable or disable navigation buttons depending on version history.
        """
        model = self.context.data_model
        has_history = model and len(model.history) > 0
        was_anomaly_removed = getattr(model, 'anomalies_removed', False)
        self.set_original_button_enabled(has_history or was_anomaly_removed)