from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class BaseGraphTab(QWidget):
    """Base class for all graph tabs"""
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.panel = None
        self._init_canvas()
        
    def _init_canvas(self):
        """Initialize matplotlib canvas"""
        self.figure = Figure(figsize=(6, 3))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    def draw(self, data):
        """Main drawing method to be implemented by subclasses"""
        raise NotImplementedError
        
    def clear(self):
        """Clear the canvas"""
        self.ax.clear()
        self.canvas.draw()

    def set_context(self, panel):
        self.panel = panel

    def apply_default_style(self, ax, x_label, y_label):
        ax.set_facecolor('#f0f8ff')
        ax.grid(color='#b0e0e6', linestyle='--', alpha=0.7)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
