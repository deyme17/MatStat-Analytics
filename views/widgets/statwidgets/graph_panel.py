from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox, QCheckBox, QTabWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from utils.def_bins import get_default_bin_count
from PyQt6.QtWidgets import QScrollArea, QWidget

from views.widgets.statwidgets.stat_dist_selector import DistributionSelector
from services.ui_services.graph_plotter import GraphPlotter


class GraphPanel(QWidget):
    def __init__(self, window, on_dist_change=None):
        super().__init__(window)
        self.window = window

        self.hist_canvas, self.hist_ax = self._create_canvas("Histogram")
        self.edf_canvas, self.edf_ax = self._create_canvas("Empirical Distribution Function")

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

        self.dist_selector = DistributionSelector(on_change=on_dist_change or self.plot_all)
        self.graph_plotter = GraphPlotter(self)

        self._init_layout()

        self.bins_spinbox.valueChanged.connect(self.plot_all)
        self.confidence_spinbox.valueChanged.connect(self.plot_all)
        self.show_additional_kde.stateChanged.connect(self.plot_all)

        self.data = None

    def _create_canvas(self, title):
        fig = Figure(figsize=(6, 3))
        ax = fig.add_subplot(111)
        canvas = FigureCanvas(fig)
        return canvas, ax

    def _init_layout(self):
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

        # params
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

    def plot_all(self):
        if self.data is not None:
            self.graph_plotter.plot_all()

    def set_data(self, data):
        self.data = data

        self.bins_spinbox.setMaximum(len(data))
        default_bins = get_default_bin_count(data)
        self.bins_spinbox.setValue(default_bins)

        self.plot_all()

    def get_selected_distribution(self):
        return self.dist_selector.get_selected_distribution()
    
    def clear(self):
        self.hist_ax.clear()
        self.edf_ax.clear()
        self.hist_canvas.draw()
        self.edf_canvas.draw()
