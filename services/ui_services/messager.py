from PyQt6.QtWidgets import QMessageBox, QWidget

class UIMessager:
    def __init__(self, parent: QWidget = None):
        self.parent = parent

    def show_info(self, title: str, message: str):
        QMessageBox.information(self.parent, title, message)

    def show_error(self, title: str, message: str):
        QMessageBox.critical(self.parent, title, message)