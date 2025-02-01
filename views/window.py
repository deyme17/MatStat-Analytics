from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout,
    QSpinBox, QLabel
)
from PyQt6.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from models.data_model import Data
from controllers.data_loader import load_data_file
from controllers.plot_controller import plot_histogram

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MatStat')
        self.setWindowIcon(QIcon("resources/MatStat.jpeg"))
        self.resize(900, 600)

        # Initialize data model
        self.data_model = Data()
        self.data = None

        # Create widgets
        self.load_data_button = QPushButton('Load Data')
        self.load_data_button.setFixedSize(80, 30)
        self.load_data_button.clicked.connect(lambda: load_data_file(self))

        # Bins control
        self.bins_label = QLabel('Number of Classes:')
        self.bins_spinbox = QSpinBox()
        self.bins_spinbox.setRange(1, 100)
        self.bins_spinbox.setValue(10)
        self.bins_spinbox.setEnabled(False)

        # Plot button
        self.plot_button = QPushButton('Plot Histogram')
        self.plot_button.setEnabled(False)
        self.plot_button.clicked.connect(lambda: plot_histogram(self))

        # Create matplotlib figure with adjusted size
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        # Layout setup
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.load_data_button)
        controls_layout.addWidget(self.bins_label)
        controls_layout.addWidget(self.bins_spinbox)
        controls_layout.addWidget(self.plot_button)
        controls_layout.addStretch()

        ver_layout = QVBoxLayout()
        ver_layout.addLayout(controls_layout)
        ver_layout.addWidget(self.canvas)

        central_widget = QWidget()
        central_widget.setLayout(ver_layout)
        self.setCentralWidget(central_widget)