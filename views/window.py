from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QTabWidget, QMessageBox
from PyQt6.QtGui import QIcon, QPalette, QColor

from controllers.data_controllers.data_loader import load_data_file
from controllers.ui_controllers.graph_controller import GraphController

from views.tabs.data_processing_tab import DataProcessingTab
from views.tabs.stat_table_tab import StatisticTab
from views.tabs.gof_test_tab import GOFTestTab
from views.widgets.statwidgets.graph_panel import GraphPanel
from views.widgets.window_widget import WindowWidgets
from utils.ui_styles import appStyle
from factory import Factory


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MatStat Analytics')
        self.setWindowIcon(QIcon("resources/MatStat.jpeg"))
        self.resize(1400, 800)

        self._init_palette()
        self.setStyleSheet(appStyle)

        # Data
        self.data_model = None

        # add controllers and services
        Factory.create(self)

        # Widgets
        self.widgets = WindowWidgets(self)
        self.graph_panel = GraphPanel(self, on_dist_change=self.evaluate_distribution_change)
        self.graph_controller = GraphController(self.graph_panel)

        # UI Tabs
        self._create_tabs()
        self._create_layout()

    def _init_palette(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 248, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(245, 250, 255))
        self.setPalette(palette)

    def _create_tabs(self):
        self.left_tab_widget = QTabWidget()
        self.data_tab = DataProcessingTab(self)
        self.stat_tab = StatisticTab()
        self.gof_tab = GOFTestTab(self)

        self.left_tab_widget.addTab(self.data_tab, "Data Processing")
        self.left_tab_widget.addTab(self.stat_tab, "Statistic")
        self.left_tab_widget.addTab(self.gof_tab, "Goodness-of-Fit Tests")

    def _create_layout(self):
        main_panel = QHBoxLayout()
        main_panel.addWidget(self.left_tab_widget, stretch=1)
        main_panel.addWidget(self.graph_panel, stretch=3)

        main_layout = QVBoxLayout()

        controls_bar = self.widgets.create_controls_bar()
        self.precision_spinbox.valueChanged.connect(lambda: self.stat_controller.update_statistics_table())
        self.load_data_button.clicked.connect(lambda: load_data_file(self))

        main_layout.addLayout(controls_bar)
        main_layout.addLayout(main_panel, stretch=1)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def evaluate_distribution_change(self):
        if not hasattr(self, "graph_panel") or not hasattr(self, "gof_tab"):
            return
        if self.data_model is None or self.data_model.series.empty:
            return
        self.graph_panel.plot_all()
        selected_dist = self.graph_panel.get_selected_distribution()
        if selected_dist is None:
            self.gof_tab.clear_tests()
        else:
            self.gof_tab.evaluate_tests()

    def _create_nav_layout(self):
        return self.widgets.create_nav_layout()

    def show_error_message(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_info_message(self, title, message):
        QMessageBox.information(self, title, message)