from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtGui import QIcon, QPalette, QColor

from utils.ui_styles import appStyle
from utils.app_context import AppContext
from factory import Factory

WIN_ICON_PATH = "resources/MatStat.jpeg"
WIN_TITLE_PATH = "MatStat Analytics"

WIN_WIDTH, WIN_HEIGHT = 1400, 700
WIN_PALETTE_R, WIN_PALETTE_B, WIN_PALETTE_G = 240, 248, 255
BASE_PALETTE_R, BASE_PALETTE_B, BASE_PALETTE_G = 245, 250, 255


class Window(QMainWindow):
    """Main application window for the MatStat Analytics tool."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WIN_TITLE_PATH)
        self.setWindowIcon(QIcon(WIN_ICON_PATH))
        self.resize(WIN_WIDTH, WIN_HEIGHT)

        self._init_palette()
        self.setStyleSheet(appStyle)

        self.context = AppContext()
        Factory.create(self, self.context)

        self._create_layout()

    def _init_palette(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(WIN_PALETTE_R, WIN_PALETTE_B, WIN_PALETTE_G))
        palette.setColor(QPalette.ColorRole.Base, QColor(BASE_PALETTE_R, BASE_PALETTE_B, BASE_PALETTE_G))
        self.setPalette(palette)

    def _create_layout(self):
        main_panel = QHBoxLayout()
        main_panel.addWidget(self.left_tab_widget, stretch=1)
        main_panel.addWidget(self.graph_panel, stretch=3)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.controls_bar.layout)
        main_layout.addLayout(main_panel)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
