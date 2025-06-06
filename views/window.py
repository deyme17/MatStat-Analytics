from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QTabWidget, QMessageBox
from PyQt6.QtGui import QIcon, QPalette, QColor

from views.tabs.data_processing_tab import DataProcessingTab
from views.tabs.stat_table_tab import StatisticTab
from views.tabs.gof_test_tab import GOFTestTab
from views.tabs.simulation_tab import SimulationTab
from views.tabs.params_estimation_tab import ParamEstimationTab

from views.widgets.window_widget import WindowWidgets
from utils.ui_styles import appStyle
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

        # Data model for currently loaded dataset
        self.data_model = None

        # Register controllers and services via Factory
        Factory.create(self)

        # UI Widget
        self.widgets = WindowWidgets(self)

        # UI Tabs
        self._create_tabs()
        self._create_layout()

    def _init_palette(self):
        """
        Configure the application’s color palette using light tones.
        """
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 248, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(245, 250, 255))
        self.setPalette(palette)

    def _create_tabs(self):
        """
        Create and add the main application tabs.
        """
        self.left_tab_widget = QTabWidget()
        self.data_tab = DataProcessingTab(self)
        self.stat_tab = StatisticTab()
        self.gof_tab = GOFTestTab(self)
        self.sim_tab = SimulationTab(self)
        self.est_tab = ParamEstimationTab(self)

        self.left_tab_widget.addTab(self.data_tab, "Data Processing")
        self.left_tab_widget.addTab(self.stat_tab, "Statistic")
        self.left_tab_widget.addTab(self.gof_tab, "Goodness-of-Fit Tests")
        self.left_tab_widget.addTab(self.sim_tab, "Simulation")
        self.left_tab_widget.addTab(self.est_tab, "Parameters estimation")

    def _create_layout(self):
        """
        Define and apply the main layout including tabs, graph panel and controls.
        """
        main_panel = QHBoxLayout()
        main_panel.addWidget(self.left_tab_widget, stretch=1)
        main_panel.addWidget(self.graph_panel, stretch=3)

        main_layout = QVBoxLayout()
        controls_bar = self.widgets.create_controls_bar()

        self.precision_spinbox.valueChanged.connect(
            lambda: self.stat_controller.update_statistics_table()
        )
        self.load_data_button.clicked.connect(
            lambda: self.data_load_controller.load_data_file()
        )

        main_layout.addLayout(controls_bar)
        main_layout.addLayout(main_panel, stretch=1)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def _create_nav_layout(self):
        """
        Proxy method to create a navigation layout from widget utilities.
        """
        return self.widgets.create_nav_layout()

    def show_error_message(self, title, message):
        """
        Display an error popup with the given title and message.
        """
        QMessageBox.critical(self, title, message)

    def show_info_message(self, title, message):
        """
        Display an informational popup with the given title and message.
        """
        QMessageBox.information(self, title, message)
