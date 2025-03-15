import sys
from PyQt6.QtWidgets import QApplication
from models.data_model import Data
from models.data_processor import DataProcessor
from views.window import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)

    data_model = Data()
    data_processor = DataProcessor()
    window = Window(data_model, data_processor)
    window.show()

    sys.exit(app.exec())