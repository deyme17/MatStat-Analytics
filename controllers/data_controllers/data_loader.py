import os
from typing import Callable
from utils.helpers import get_default_bin_count

from utils import AppContext, EventType, EventBus
from services import DataLoaderService, UIMessager, DataVersionManager
from models.data_model import DataModel


class DataLoadController:
    """
    Controller for managing data loading operations and notifying the app of updates.
    """
    def __init__(
        self,
        context: AppContext,
        loader_service: DataLoaderService,
        select_file_callback: Callable[[], str | None],
    ):
        """
        Args:
            context: Shared application state and dependencies
            loader_service: Service for selecting and loading data
            select_file_callback: Function to show file dialog and return file path
        """
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.messanger: UIMessager = context.messanger
        self.version_manager: DataVersionManager = context.version_manager
        self.loader_service: DataLoaderService = loader_service
        self.select_file_callback = select_file_callback
        self.data_model_class = DataModel

    def load_data_file(self) -> None:
        """
        Load a data file selected by the user and initialize the DataModel.
        """
        path = self.select_file_callback()
        if not path:
            return

        filename_ext = os.path.basename(path)
        filename = self._build_filename(filename_ext)

        data = self.loader_service.load_data(path)

        if data is None or data.empty:
            self.messanger.show_info(f"Failed to load file {path} or file is empty")
            return

        # Create new data model and update context
        bin_count = get_default_bin_count(data)
        model = self.data_model_class(data, bins=bin_count, label="Original")
        self.version_manager.add_dataset(filename, model)
        self.context.data_model = model
        self.event_bus.emit_type(EventType.DATA_LOADED, model.series)

    def _build_filename(self, filename_ext: str) -> str:
        """
        Creates unique filename for dataset
        """
        name, ext = os.path.splitext(filename_ext)
        current_filenames = self.version_manager.get_all_dataset_names()
        counter = 1
        new_filename = filename_ext
        while new_filename in current_filenames:
            new_filename = f"{name}_{counter}{ext}"
            counter += 1
        return new_filename