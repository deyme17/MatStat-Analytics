from services.data_services.data_loader_service import DataLoaderService
from models.data_model import DataModel
from utils.def_bins import get_default_bin_count
import os

def load_data_file(window):
    """
    Load a data file selected by the user and initialize the DataModel.

    :param window: main application window
    """
    path = DataLoaderService.select_file(window)
    if not path:
        return

    filename, data = os.path.basename(path), DataLoaderService.load_data(path)

    if data is None or data.empty:
        print(f"Failed to load file {path} or file is empty")
        return

    bin_count = get_default_bin_count(data)
    model = DataModel(data, bins=bin_count, label="Original")
    window.version_manager.add_dataset(filename, model)
    window.data_model = model

    DataLoaderService.postprocess_loaded_data(window, data)
    window.original_button.setEnabled(False)

    print(f'File {path} selected successfully')
