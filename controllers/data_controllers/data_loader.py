from utils.def_bins import get_default_bin_count
from models.data_model import DataModel
import os

class DataLoadController:
    """
    Controller for managing data loading operations and UI updates.
    """
    def __init__(self, window, loader_service):
        """
        Args:
            window (QWidget): Reference to the main application window
            loader_service: Service for data loading operations
        """
        self.window = window
        self.loader_service = loader_service
        self.data_model = DataModel()
        
    def load_data_file(self):
        """
        Load a data file selected by the user and initialize the DataModel.
        """
        path = self.loader_service.select_file(self.window)
        if not path:
            return

        filename, data = os.path.basename(path), self.loader_service.load_data(path)

        if data is None or data.empty:
            print(f"Failed to load file {path} or file is empty")
            return

        bin_count = get_default_bin_count(data)
        model = self.data_model(data, bins=bin_count, label="Original")
        self.window.version_manager.add_dataset(filename, model)
        self.window.data_model = model

        self.window.state_controller.handle_post_load_state(data)
        self.window.original_button.setEnabled(False)

        print(f'File {path} selected successfully')
