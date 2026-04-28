from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

DIALOG_WIDTH = 700
DIALOG_HEIGHT = 600


class ResidualsFittedPlot(QDialog):
    """
    Modal dialog for visualizing residuals and fitted values.
    It used as diagnostics plot for regression models, showing residuals vs fitted values.
    """
    def __init__(self, residuals: np.ndarray, fitted: np.ndarray, parent=None):
        """
        Args:
            residuals: Residuals from regression model.    
            fitted: Fitted values from regression model.
            parent: Parent widget.
        """
        super().__init__(parent)

        self.setWindowTitle("Residuals vs Fitted plot for regression diagnostics")
        self.setFixedSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self._init_ui()
        self._plot(residuals, fitted)

    def _init_ui(self) -> None:
        layout = QVBoxLayout()

        self.figure = Figure(figsize=(6, 5), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # close button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def _plot(self, residuals: np.ndarray, fitted: np.ndarray) -> None:
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.scatter(residuals, fitted, alpha=0.7)
        ax.set_xlabel("Residuals")
        ax.set_ylabel("Fitted Values")
        ax.set_title("Residuals vs Fitted Values")
        ax.grid(True, linestyle='--', alpha=0.5)
        self.canvas.draw()
