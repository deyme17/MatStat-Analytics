from services.data_loader_service import DataLoaderService
import os

def load_data_file(window):
    path = DataLoaderService.select_file(window)
    if not path:
        return

    filename, data = os.path.basename(path), DataLoaderService.load_data(path)

    if data is None or data.empty:
        print(f"Failed to load file {path} or file is empty")
        return

    DataLoaderService.postprocess_loaded_data(window, filename, data)

    window.data = window.version_manager.get_current_data()
    window.graph_controller.set_data(window.data)
    window.stat_controller.update_statistics_table()
    print(f'File {path} selected successfully')
