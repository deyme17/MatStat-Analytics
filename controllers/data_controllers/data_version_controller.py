from typing import Callable, Optional
from callbacks.ui_versions_callbacks import DataVersionUICallbacks
import pandas as pd


class DataVersionController:
    """
    Controller for managing dataset versions (original and transformed).
    """
    def __init__(
        self,
        context,
        version_combo_controls: Optional[DataVersionUICallbacks] = None,
        set_bins_value: Optional[Callable[[int], None]] = None,
        update_navigation_buttons: Optional[Callable[[], None]] = None,
        on_reverted_to_original: Optional[Callable[[], None]] = None,
        on_version_changed: Optional[Callable[[pd.Series], None]] = None
    ):
        """
        Args:
            context: Shared application context (data, history, refresher, etc.)
            version_combo_controls: Container of version_combo_controls control callbacks
            set_bins_value: Function for setting bin count configuration
            update_navigation_buttons: Callback triggered after version selected
            on_reverted_to_original: Callback triggered after reverting to original data
            on_version_changed: Callback triggered after version is changed
        """
        self.context = context
        self.version_combo_controls = version_combo_controls
        self.set_bins_value = set_bins_value
        self.update_navigation_buttons = update_navigation_buttons
        self.on_reverted_to_original = on_reverted_to_original
        self.on_version_changed = on_version_changed

    def on_data_version_changed(self, index: int) -> None:
        """
        Called when the user selects a different version from the dropdown.
        """
        self.check_all_connected()
        labels = self.context.version_manager.get_all_descriptions()
        if 0 <= index < len(labels):
            label = labels[index]
            self.context.version_manager.switch_to(label)
            self.context.data_model = self.context.version_manager.get_current_data()
            self._update_all()

    def original_data(self) -> None:
        """
        Revert to the original dataset version and update UI accordingly.
        """
        self.check_all_connected()
        original = self.context.version_manager.get_original_data()
        if original:
            self.context.data_model = original
            self.context.version_manager.update_current_data(original)
            self.on_reverted_to_original()
            self.context.refresher.refresh(original.series)
            self.on_version_changed(original.series)

    def update_data_versions(self) -> None:
        """
        Update dropdown menu with all available data versions.
        """
        self.check_all_connected()
        labels = self.context.version_manager.get_all_descriptions()
        
        self.version_combo_controls.block_signals(True)
        self.version_combo_controls.set_version_list(labels)

        current = self.context.version_manager.get_data_description()
        if current in labels:
            self.version_combo_controls.set_current_index(labels.index(current))

        self.version_combo_controls.block_signals(False)
        self._update_all()

    def update_data_version_selection(self) -> None:
        """
        Sync the dropdown selection with the currently active dataset.
        """
        self.check_all_connected()
        labels = self.context.version_manager.get_all_descriptions()
        current = self.context.version_manager.get_data_description()

        self.version_combo_controls.block_signals(True)
        if current in labels:
            self.version_combo_controls.set_current_index(labels.index(current))
        self.version_combo_controls.block_signals(False)

        self.update_navigation_buttons()

    def _update_all(self) -> None:
        """
        Internal helper to refresh UI after switching dataset.
        """
        self.check_all_connected()
        series = self.context.data_model.series
        self.set_bins_value(self.context.data_model.bins)
        self.context.refresher.refresh(series)
        self.on_version_changed(series)

    def connect_callbacks(self, version_combo_controls: DataVersionUICallbacks,
                                update_navigation_buttons: Callable[[], None],
                                on_reverted_to_original: Callable[[], None],
                                on_version_changed: Callable[[pd.Series], None]) -> None:
        self.version_combo_controls = version_combo_controls
        self.update_navigation_buttons = update_navigation_buttons
        self.on_reverted_to_original = on_reverted_to_original
        self.on_version_changed = on_version_changed

    def set_set_bins_value_func(self, set_bins_value: Callable[[int], None]):
        self.set_bins_value = set_bins_value
        
    def check_all_connected(self) -> None:
        if not (self.version_combo_controls and self.set_bins_value and self.update_navigation_buttons 
                and self.on_reverted_to_original and self.on_version_changed):
            raise RuntimeError("Not all ui functions&callbacks connected to DataVersionController")