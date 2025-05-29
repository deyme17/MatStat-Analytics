from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox, QCheckBox, QTabWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from utils.def_bins import get_default_bin_count
from PyQt6.QtWidgets import QScrollArea, QWidget

from services.ui_services.ui_refresh_service import UIRefreshService
from models.stat_distributions.stat_distribution import StatisticalDistribution
import pandas as pd

from views.widgets.statwidgets.stat_dist_selector import DistributionSelector
from services.ui_services.graph_plotter import GraphPlotter


class GraphPanel(QWidget):
    """
    A visual panel for displaying statistical plots.
    """

    def __init__(self, window, on_dist_change=None):
        super().__init__(window)
        self.window = window
        self.data = None

        # Initialize canvases
        self.hist_canvas, self.hist_ax = self._create_canvas("Histogram")
        self.edf_canvas, self.edf_ax = self._create_canvas("Empirical Distribution Function")

        # UI elements
        self.bins_spinbox = QSpinBox()
        self.bins_spinbox.setRange(1, 999)
        self.bins_spinbox.setValue(10)
        self.bins_spinbox.setMaximumWidth(100)

        self.confidence_spinbox = QDoubleSpinBox()
        self.confidence_spinbox.setRange(0.80, 0.99)
        self.confidence_spinbox.setSingleStep(0.01)
        self.confidence_spinbox.setValue(0.95)
        self.confidence_spinbox.setDecimals(2)

        self.show_additional_kde = QCheckBox("Show additional KDE")
        self.show_additional_kde.setChecked(False)

        self.dist_selector = DistributionSelector(on_change=self.refresh_all)
        self.graph_plotter = GraphPlotter(self)

        self._init_layout()

        # Connect controls
        self.bins_spinbox.valueChanged.connect(self.refresh_all)
        self.confidence_spinbox.valueChanged.connect(self.refresh_all)
        self.show_additional_kde.stateChanged.connect(self.refresh_all)

    def _create_canvas(self, title: str) -> tuple:
        """
        Create a matplotlib canvas and axis.
        """
        fig = Figure(figsize=(6, 3))
        ax = fig.add_subplot(111)
        canvas = FigureCanvas(fig)
        return canvas, ax

    def _init_layout(self):
        """
        Build the panel layout with tabs and control widgets.
        """
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Histogram tab
        hist_layout = QVBoxLayout()
        hist_layout.addWidget(self.hist_canvas)
        hist_widget = QWidget()
        hist_widget.setLayout(hist_layout)
        self.tabs.addTab(hist_widget, "Histogram")

        # EDF tab
        edf_layout = QVBoxLayout()
        edf_layout.addWidget(self.edf_canvas)
        edf_widget = QWidget()
        edf_widget.setLayout(edf_layout)
        self.tabs.addTab(edf_widget, "Empirical distribution function")

        layout.addWidget(self.tabs)

        # Parameter controls
        params_layout = QHBoxLayout()
        params_layout.addWidget(QLabel("Bins:"))
        params_layout.addWidget(self.bins_spinbox)
        params_layout.addSpacing(20)
        params_layout.addWidget(QLabel("Confidence Level (CI):"))
        params_layout.addWidget(self.confidence_spinbox)
        params_layout.addStretch()
        params_layout.addWidget(self.show_additional_kde)

        layout.addLayout(params_layout)
        layout.addWidget(self.dist_selector)

        self.setLayout(layout)

    def refresh_all(self):
        if self.data is not None:
            self.window.data_model.update_bins(self.bins_spinbox.value())
            UIRefreshService.refresh_all(self.window, self.data)

    def set_data(self, data: pd.Series):
        self.data = data
        self.bins_spinbox.setMaximum(len(data))
        default_bins = get_default_bin_count(data)
        self.bins_spinbox.setValue(default_bins)
        self.refresh_all()

    def get_selected_distribution(self) -> StatisticalDistribution:
        """
        Return the currently selected distribution class.
        """
        return self.dist_selector.get_selected_distribution()

    def clear(self):
        """
        Clear both plots from the canvas.
        """
        self.hist_ax.clear()
        self.edf_ax.clear()
        self.hist_canvas.draw()
        self.edf_canvas.draw()
