from PyQt6.QtWidgets import QFileDialog
from controllers.plot_controller import set_default_bins

def load_data_file(window):
    path, _ = QFileDialog.getOpenFileName(
        window,
        'Select the File',
        '',
        'Text Files (*.txt);;All Files (*)'
    )

    if path:
        data = window.data_model.load_data(path)

        if data is not None and not data.empty:
            window.data = data
            window.bins_spinbox.setEnabled(True)
            window.plot_button.setEnabled(True)
            window.bins_spinbox.setValue(set_default_bins(window.data))
            print(f'File {path} selected successfully')
        else:
            print(f'Failed to load file {path} or file is empty')