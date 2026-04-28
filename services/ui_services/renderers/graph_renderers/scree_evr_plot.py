from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from typing import List

DIALOG_WIDTH = 700
DIALOG_HEIGHT = 600


class ScreeEVRPlot(QDialog):
    """
    Modal dialog for visualizing scree plot of Explained Variance Ratio.
    It shows the proportion of data variance accounted by each principal component.
    """
    def __init__(self, evr: List[float], parent=None):
        """
        Args:
            evr: Explained Variance Ratios for each principal component.    
            parent: Parent widget.
        """
        super().__init__(parent)

        self.setWindowTitle("Scree Plot for EVR visualization")
        self.setFixedSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self._init_ui()
        self._plot(evr)

    def _init_ui(self) -> None:
        layout = QVBoxLayout()

        self.figure = Figure(figsize=(8, 5), tight_layout=True)
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

    def _plot(self, evr: List[float]) -> None:
        ax = self.figure.add_subplot(111)
        ax.clear()
        pc_labels = [f"PC_{i+1}" for i in range(len(evr))]
        bars = ax.bar(pc_labels, evr, alpha=0.3, label='Individual variance')
        ax.plot(pc_labels, np.cumsum(evr), '-o', c="r", alpha=0.5, label='Cumulative variance')
        # EVR labels
        for bar, val in zip(bars, evr):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() / 2,
                f"{val:.3f}",
                ha='center',
                va='bottom',
                fontsize=9
            )
        ax.set_ylabel('Explained variance ratio')
        ax.set_xlabel('Principal component')
        ax.legend(loc='best')
        ax.grid(True, linestyle='--', alpha=0.3)
        self.canvas.draw()