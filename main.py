import sys
from PyQt6.QtWidgets import QApplication
from views.window import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = Window()
    window.show()

    sys.exit(app.exec())