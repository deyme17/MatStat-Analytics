from typing import Callable, Optional
from callbacks.combo_callbacks import ComboUICallbacks
import pandas as pd


class DataVersionController:
    """
    Controller for managing dataset selection (switching between different loaded files).
    Each dataset maintains its own transformation history via DataModel.
    """
    def __init__(
        self,
        context,
        version_combo_controls: Optional[ComboUICallbacks] = None,
        columns_combo_control: Optional[ComboUICallbacks] = None,
        set_bins_value: Optional[Callable[[int], None]] = None,
        update_navigation_buttons: Optional[Callable[[], None]] = None,
        on_reverted_to_original: Optional[Callable[[], None]] = None,
        on_dataset_changed: Optional[Callable[[pd.Series], None]] = None
    ):
        """
        Args:
            context: Shared application context (data, history, refresher, etc.)
            version_combo_controls: Container of dataset combo control callbacks
            columns_combo_control: Container of column changing combo control callbacks
            set_bins_value: Function for setting bin count configuration
            update_navigation_buttons: Callback triggered after dataset selected
            on_reverted_to_original: Callback triggered after reverting to original data
            on_dataset_changed: Callback triggered after dataset is changed
        """
        self.context = context
        self.version_combo_controls = version_combo_controls
        self.columns_combo_control = columns_combo_control
        self.set_bins_value = set_bins_value
        self.update_navigation_buttons = update_navigation_buttons
        self.on_reverted_to_original = on_reverted_to_original
        self.on_dataset_changed = on_dataset_changed

    def on_dataset_selection_changed(self, index: int) -> None:
        """
        Called when the user selects a different dataset from the dropdown.
        """
        self.check_all_connected()
        dataset_names = self.context.version_manager.get_all_dataset_names()
        
        if 0 <= index < len(dataset_names):
            dataset_name = dataset_names[index]
            self.context.version_manager.switch_to_dataset(dataset_name)
            self.context.data_model = self.context.version_manager.get_current_data_model()
            self._update_all_ui()

    def on_current_col_changed(self, index: int) -> None:
        """
        Called when the user changes a different coloumn from the dropdown.
        """
        self.check_all_connected()
        dataset_name = self.context.version_manager.get_current_dataset_name()
        col_names = self.context.version_manager.get_all_columns_names(dataset_name)
        
        if 0 <= index < len(col_names):
            col_name = col_names[index]
            self.context.version_manager.change_column(col_name)
            col_idx = self.context.data_model.dataframe.columns.get_loc(col_name)
            self.context.data_model.select_column(col_idx)
            assert self.context.data_model.current_col_idx == col_idx
            self._update_all_ui()

    def revert_to_original(self, whole_dataset: bool = False) -> None:
        """
        Revert current dataset to its original version.
        """
        self.check_all_connected()
        if self.context.data_model:
            original = self.context.data_model.revert_to_original(whole_dataset)
            self.context.version_manager.update_current_dataset(original)
            self.context.data_model = original

            self.on_reverted_to_original()
            self.context.refresher.refresh(original.series)
            self.on_dataset_changed(original.series)

    def update_dataset_list(self) -> None:
        """
        Update dropdown menu with all available datasets.
        """
        self.check_all_connected()
        dataset_names = self.context.version_manager.get_all_dataset_names()
        
        self.version_combo_controls.block_signals(True)
        self.version_combo_controls.set(dataset_names)

        current_name = self.context.version_manager.get_current_dataset_name()
        if current_name in dataset_names:
            self.version_combo_controls.set_current_index(dataset_names.index(current_name))

        self.version_combo_controls.block_signals(False)

        self.update_columns_list()
        self._update_all_ui()

    def update_columns_list(self):
        """
        Update dropdown menu with all available dataset's columns.
        """
        self.check_all_connected()
        dataset_name = self.context.version_manager.get_current_dataset_name()
        if not dataset_name:
            return
        col_names = self.context.version_manager.get_all_columns_names(dataset_name)

        self.columns_combo_control.block_signals(True)
        self.columns_combo_control.set(col_names)

        current_col = self.context.version_manager.get_current_column_name()
        if current_col in col_names:
            self.columns_combo_control.set_current_index(col_names.index(current_col))
        else:
            self.columns_combo_control.set_current_index(0)
            self.context.version_manager.change_column(col_names[0])

        self.columns_combo_control.block_signals(False)

    def update_dataset_selection(self) -> None:
        """
        Sync the dropdown selection with the currently active dataset.
        """
        self.check_all_connected()
        dataset_names = self.context.version_manager.get_all_dataset_names()
        current_name = self.context.version_manager.get_current_dataset_name()

        self.version_combo_controls.block_signals(True)
        if current_name in dataset_names:
            self.version_combo_controls.set_current_index(dataset_names.index(current_name))
        self.version_combo_controls.block_signals(False)

        self.update_navigation_buttons()

    def _update_all_ui(self) -> None:
        """
        Internal helper to refresh UI after switching dataset.
        """
        self.check_all_connected()
        if self.context.data_model:
            series = self.context.data_model.series
            self.set_bins_value(self.context.data_model.bins)
            self.context.refresher.refresh(series)
            self.on_dataset_changed(series)

    def has_transformation_history(self) -> bool:
        """
        Check if current dataset has any transformations applied.
        """
        return (self.context.data_model and 
                len(self.context.data_model.history) > 0)

    def get_current_transformation_info(self) -> str:
        """
        Get description of current transformation state.
        """
        if self.context.data_model:
            return self.context.data_model.current_transformation
        return "No Data"

    def connect_callbacks(self, 
                         version_combo_controls: ComboUICallbacks,
                         columns_combo_control: ComboUICallbacks,
                         update_navigation_buttons: Callable[[], None],
                         on_reverted_to_original: Callable[[], None],
                         on_dataset_changed: Callable[[pd.Series], None]) -> None:
        self.version_combo_controls = version_combo_controls
        self.columns_combo_control = columns_combo_control
        self.update_navigation_buttons = update_navigation_buttons
        self.on_reverted_to_original = on_reverted_to_original
        self.on_dataset_changed = on_dataset_changed

    def set_set_bins_value_func(self, set_bins_value: Callable[[int], None]):
        self.set_bins_value = set_bins_value
        
    def check_all_connected(self) -> None:
        if not (self.version_combo_controls and self.columns_combo_control and self.set_bins_value 
                and self.update_navigation_buttons and self.on_reverted_to_original and self.on_dataset_changed):
            raise RuntimeError("Not all ui functions&callbacks connected to DataVersionController")