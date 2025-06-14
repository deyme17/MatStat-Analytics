import os
import pandas as pd
from typing import Callable
from utils.def_bins import get_default_bin_count
from models.data_model import DataModel


class DataLoadController:
    """
    Controller for managing data loading operations and notifying the app of updates.
    """

    def __init__(
        self,
        context,
        loader_service,
        select_file_callback: Callable[[], str | None],
        on_data_loaded_callback: Callable[[pd.Series], None]
    ):
        """
        Args:
            context: Shared application state and dependencies
            loader_service: Service for selecting and loading data
            select_file_callback: Function to show file dialog and return file path
            on_data_loaded_callback: Callback to notify when data has been successfully loaded
        """
        self.context = context
        self.loader_service = loader_service
        self.select_file_callback = select_file_callback
        self.on_data_loaded = on_data_loaded_callback
        self.data_model_class = DataModel

    def load_data_file(self) -> None:
        """
        Load a data file selected by the user and initialize the DataModel.
        """
        path = self.select_file_callback()
        if not path:
            return

        filename = os.path.basename(path)
        data = self.loader_service.load_data(path)

        if data is None or data.empty:
            print(f"❌ Failed to load file {path} or file is empty")
            return

        # Create new data model and update context
        bin_count = get_default_bin_count(data)
        model = self.data_model_class(data, bins=bin_count, label="Original")
        self.context.version_manager.add_dataset(filename, model)
        self.context.data_model = model

        self.on_data_loaded(data)

        print(f"✅ File {path} loaded successfully")
