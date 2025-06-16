from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QIcon, QPalette, QColor

from utils.ui_styles import appStyle
from app_context import AppContext
from factory import Factory

class Window(QMainWindow):
    """
    Main application window for the MatStat Analytics tool.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MatStat Analytics')
        self.setWindowIcon(QIcon("resources/MatStat.jpeg"))
        self.resize(1400, 800)

        self._init_palette()
        self.setStyleSheet(appStyle)

        self.data_model = None
        self.context = AppContext()
        Factory.create(self, self.context)

        self._create_layout()

    def _init_palette(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 248, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(245, 250, 255))
        self.setPalette(palette)

    def _create_layout(self):
        main_panel = QHBoxLayout()
        main_panel.addWidget(self.left_tab_widget, stretch=1)
        main_panel.addWidget(self.graph_panel, stretch=3)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.controls_layout)
        main_layout.addLayout(main_panel)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
