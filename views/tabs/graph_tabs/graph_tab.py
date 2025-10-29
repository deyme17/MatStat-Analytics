from abc import abstractmethod
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from models.data_model import DataModel
from utils import AppContext

FIG_SIZE = (6, 3)
GRID_ALPHA = 0.7
GRID_COLOR = '#b0e0e6'
FIG_COLOR = '#f0f8ff'


class BaseGraphTab(QWidget):
    """Base class for graph tabs"""
    def __init__(self, name: str, context: AppContext):
        """
        Args:
            name: Tab name
            context: Application context
        """
        super().__init__()
        self.name = name
        self.context = context
        self.panel = None
        self._init_canvas()
    
    def _init_canvas(self) -> None:
        """Initialize matplotlib canvas"""
        self.figure = Figure(figsize=FIG_SIZE)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    @abstractmethod
    def draw(self) -> None:
        """Main drawing method to be implemented by subclasses"""
        raise NotImplementedError
    
    def clear(self) -> None:
        """Clear the canvas"""
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.colorbar = None
        self.canvas.draw()

    def set_panel(self, panel) -> None:
        """Set reference to parent panel"""
        self.panel = panel

    def get_data_model(self) -> DataModel:
        """Get current data model from context"""
        return self.context.data_model

    def apply_default_style(self, ax: plt.Axes, x_label: str, y_label: str) -> None:
        """Apply default styling to axes"""
        ax.set_facecolor(FIG_COLOR)
        ax.grid(color=GRID_COLOR, linestyle='--', alpha=GRID_ALPHA)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)