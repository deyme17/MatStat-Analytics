import sys
from utils.ui_styles import apply_light_palette, TABLE_STYLE
from PyQt6.QtWidgets import QApplication
from views.window import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    apply_light_palette(app)
    app.setStyleSheet(app.styleSheet() + TABLE_STYLE)

    window = Window()
    window.show()

    sys.exit(app.exec())