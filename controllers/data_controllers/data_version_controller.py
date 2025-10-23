from utils import AppContext, EventType, EventBus, Event
from services.data_services.data_version_manager import DataVersionManager
from models.data_model import DataModel
from utils.combo_callbacks import ComboUICallbacks
from typing import Callable, Optional


class DataVersionController:
    """
    Controller for managing dataset selection (switching between different loaded files).
    Each dataset maintains its own transformation history via DataModel.
    """
    def __init__(
        self,
        context: AppContext,
        version_combo_controls: Optional[ComboUICallbacks] = None,
        columns_combo_control: Optional[ComboUICallbacks] = None,
        set_bins_value: Optional[Callable[[int], None]] = None
    ):
        """
        Args:
            context: Shared application context (data, history, etc.)
            version_combo_controls: Container of dataset combo control callbacks
            columns_combo_control: Container of column changing combo control callbacks
            set_bins_value: Function for setting bin count configuration
        """
        self.context: AppContext = context
        self.data_model: DataModel = context.data_model
        self.event_bus: EventBus = context.event_bus
        self.version_manager: DataVersionManager = context.version_manager
        self.version_combo_controls = version_combo_controls
        self.columns_combo_control = columns_combo_control
        self.set_bins_value = set_bins_value
        
        self._subscribe_to_events()

    def _subscribe_to_events(self):
        self.event_bus.subscribe(EventType.DATA_LOADED, self._on_data_loaded)

    def _on_data_loaded(self, event: Event):
        self.update_dataset_list()

    def on_dataset_selection_changed(self, index: int) -> None:
        """
        Called when the user selects a different dataset from the dropdown.
        """
        dataset_names = self.version_manager.get_all_dataset_names()
        
        if 0 <= index < len(dataset_names):
            dataset_name = dataset_names[index]
            self.version_manager.switch_to_dataset(dataset_name)
            self.data_model = self.version_manager.get_current_data_model()
            
            self.event_bus.emit_type(EventType.DATASET_CHANGED, {
                'model': self.data_model,
                'series': self.data_model.series
            })

    def on_current_col_changed(self, index: int) -> None:
        """
        Called when the user changes a different column from the dropdown.
        """
        dataset_name = self.version_manager.get_current_dataset_name()
        col_names = self.version_manager.get_all_columns_names(dataset_name)
        
        if 0 <= index < len(col_names):
            col_name = col_names[index]
            self.version_manager.change_column(col_name)
            col_idx = self.data_model.dataframe.columns.get_loc(col_name)
            self.data_model.select_column(col_idx)
            assert self.data_model.current_col_idx == col_idx
            
            self.event_bus.emit_type(EventType.COLUMN_CHANGED, {
                'model': self.data_model,
                'series': self.data_model.series,
                'col_name': col_name,
                'col_idx': col_idx
            })

    def revert_to_original(self, whole_dataset: bool = False) -> None:
        """
        Revert current dataset to its original version.
        """
        if self.data_model:
            original = self.data_model.revert_to_original(whole_dataset)
            self.version_manager.update_current_dataset(original)
            self.data_model = original
            
            self.event_bus.emit_type(EventType.DATA_REVERTED, {
                'model': original,
                'series': original.series,
                'whole_dataset': whole_dataset
            })

    def update_dataset_list(self) -> None:
        """
        Update dropdown menu with all available datasets.
        """
        if not self.version_combo_controls:
            return
            
        dataset_names = self.version_manager.get_all_dataset_names()
        
        self.version_combo_controls.block_signals(True)
        self.version_combo_controls.set(dataset_names)

        current_name = self.version_manager.get_current_dataset_name()
        if current_name in dataset_names:
            self.version_combo_controls.set_current_index(dataset_names.index(current_name))

        self.version_combo_controls.block_signals(False)

        self.update_columns_list()
        self._set_bins_for_new_data()

    def update_columns_list(self):
        """
        Update dropdown menu with all available dataset's columns.
        """
        if not self.columns_combo_control:
            return
            
        dataset_name = self.version_manager.get_current_dataset_name()
        if not dataset_name:
            return
        col_names = self.version_manager.get_all_columns_names(dataset_name)

        self.columns_combo_control.block_signals(True)
        self.columns_combo_control.set(col_names)

        current_col = self.version_manager.get_current_column_name()
        if current_col in col_names:
            self.columns_combo_control.set_current_index(col_names.index(current_col))
        else:
            self.columns_combo_control.set_current_index(0)
            self.version_manager.change_column(col_names[0])

        self.columns_combo_control.block_signals(False)

    def update_dataset_selection(self) -> None:
        """
        Sync the dropdown selection with the currently active dataset.
        """
        if not self.version_combo_controls:
            return
            
        dataset_names = self.version_manager.get_all_dataset_names()
        current_name = self.version_manager.get_current_dataset_name()

        self.version_combo_controls.block_signals(True)
        if current_name in dataset_names:
            self.version_combo_controls.set_current_index(dataset_names.index(current_name))
        self.version_combo_controls.block_signals(False)
        
        self.event_bus.emit_type(EventType.DATASET_CHANGED, {
            'model': self.data_model,
            'series': self.data_model.series if self.data_model else None
        })

    def get_all_datasets(self) -> dict:
        """
        Returns a dictionary of all loaded datasets {name: DataModel}
        """
        return self.version_manager.datasets

    def _set_bins_for_new_data(self) -> None:
        """
        Internal helper to refresh bins after switching dataset.
        """
        if self.data_model and self.set_bins_value:
            self.set_bins_value(self.data_model.bins)

    def has_transformation_history(self) -> bool:
        """
        Check if current dataset has any transformations applied.
        """
        return (self.data_model and 
                len(self.data_model.history) > 0)

    def get_current_transformation_info(self) -> str:
        """
        Get description of current transformation state.
        """
        if self.data_model:
            return self.data_model.current_transformation
        return "No Data"

    def connect_ui(self, 
                   version_combo_controls: ComboUICallbacks,
                   columns_combo_control: ComboUICallbacks,
                   set_bins_value: Callable[[int], None]) -> None:
        self.version_combo_controls = version_combo_controls
        self.columns_combo_control = columns_combo_control
        self.set_bins_value = set_bins_value