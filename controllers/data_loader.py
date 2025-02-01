from PyQt6.QtWidgets import QFileDialog

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
            print(f'File {path} selected successfully')
        else:
            print(f'Failed to load file {path} or file is empty')