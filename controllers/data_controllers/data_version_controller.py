from typing import Callable
import pandas as pd


class DataVersionController:
    """
    Controller for managing dataset versions (original and transformed).
    """
    def __init__(
        self,
        context,
        data_version_combo,
        bins_spinbox,
        on_reverted_to_original: Callable[[], None],
        on_version_changed: Callable[[pd.Series], None]
    ):
        """
        Args:
            context: Shared application context (data, history, refresher, etc.)
            data_version_combo: ComboBox used to select dataset versions
            bins_spinbox: SpinBox for setting histogram bin count
            on_reverted_to_original: Callback triggered after reverting to original data
            on_version_changed: Callback triggered after version is changed
        """
        self.context = context
        self.data_version_combo = data_version_combo
        self.bins_spinbox = bins_spinbox
        self.on_reverted_to_original = on_reverted_to_original
        self.on_version_changed = on_version_changed

    def on_data_version_changed(self, index: int) -> None:
        """
        Called when the user selects a different version from the dropdown.
        """
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
        original = self.context.version_manager.get_original_data()
        if original:
            self.context.data_model = original
            self.context.version_manager.update_current_data(original)

            if self.on_reverted_to_original:
                self.on_reverted_to_original()

            self.context.refresher.refresh(original.series)

    def update_data_versions(self) -> None:
        """
        Update dropdown menu with all available data versions.
        """
        self.data_version_combo.blockSignals(True)
        self.data_version_combo.clear()

        labels = self.context.version_manager.get_all_descriptions()
        self.data_version_combo.addItems(labels)

        current = self.context.version_manager.get_data_description()
        if current in labels:
            self.data_version_combo.setCurrentIndex(labels.index(current))

        self.data_version_combo.blockSignals(False)
        self._update_all()

    def update_data_version_selection(self) -> None:
        """
        Sync the dropdown selection with the currently active dataset.
        """
        labels = self.context.version_manager.get_all_descriptions()
        current = self.context.version_manager.get_data_description()

        self.data_version_combo.blockSignals(True)
        if current in labels:
            self.data_version_combo.setCurrentIndex(labels.index(current))
        self.data_version_combo.blockSignals(False)

        self.context.state_controller.update_navigation_buttons()

    def _update_all(self) -> None:
        """
        Internal helper to refresh UI after switching dataset.
        """
        series = self.context.data_model.series
        self.bins_spinbox.setValue(self.context.data_model.bins)
        self.context.refresher.refresh(series)

        if self.on_version_changed:
            self.on_version_changed(series)
