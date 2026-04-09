from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from typing import Callable
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import pandas as pd

DIALOG_WIDTH = 700
DIALOG_HEIGHT = 600


class RegressionPlotDialog(QDialog):
    """
    Modal dialog for visualizing regression results.
    Shows 2D scatter + line for 1 predictor, 3D scatter + plane for 2 predictors.
    """
    def __init__(self, X_df: pd.DataFrame, y_series: pd.Series,
                 predict_fn: Callable[[pd.DataFrame], pd.Series], 
                 interval_fn: Callable[[pd.DataFrame], pd.Series], 
                 parent=None):
        """
        Args:
            X_df:       Feature dataframe (1 or 2 columns only).
            y_series:   Target series.
            predict_fn: Callable(pd.DataFrame) -> pd.Series from controller.
            inyterval_fn: Callable(pd.DataFrame) -> pd.Series from controller.
            parent:     Parent widget.
        """
        super().__init__(parent)
        self.X_ = X_df
        self.y_ = y_series
        self.predict_fn = predict_fn
        self.interval_fn = interval_fn
        self.n_features = X_df.shape[1]

        self.setWindowTitle("Regression Visualization")
        self.setFixedSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self._init_ui()
        self._plot()

    def _init_ui(self) -> None:
        layout = QVBoxLayout()

        self.figure = Figure(figsize=(6, 5), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # info label
        mode = "2D" if self.n_features == 1 else "3D"
        self.info_label = QLabel(f"{mode} regression plot  |  n = {len(self.y_)}")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

        # close button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def _plot(self) -> None:
        if self.n_features == 1:
            self._plot_2d()
        else:
            self._plot_3d()
        self.canvas.draw()

    def _plot_2d(self) -> None:
        ax = self.figure.add_subplot(111)
        x_col = self.X_.columns[0]
        x_vals = self.X_[x_col].to_numpy()
        y_vals = self.y_.to_numpy()

        # scatter
        ax.scatter(x_vals, y_vals, alpha=0.6, edgecolors="k",
                linewidths=0.4, label="Data", zorder=3)

        # regression line
        x_line = np.linspace(x_vals.min(), x_vals.max(), 300)
        X_line_df = pd.DataFrame({x_col: x_line})
        y_line = self.predict_fn(X_line_df).to_numpy()
        ax.plot(x_line, y_line, color="crimson", linewidth=2, label="Regression line")

        if self.interval_fn is not None:
            y_lower, y_upper = self.interval_fn(X_line_df)
            ax.fill_between(x_line, y_lower, y_upper,
                            alpha=0.10, color="red")
            ax.plot(x_line, y_lower, color="red", linewidth=1,
                    linestyle="--", alpha=0.6, label="95% CI (mean)")
            ax.plot(x_line, y_upper, color="red", linewidth=1,
                    linestyle="--", alpha=0.6)

        ax.set_xlabel(x_col)
        ax.set_ylabel(self.y_.name or "y")
        ax.set_title(f"{self.y_.name or 'y'}  ~  {x_col}")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.4)

    def _plot_3d(self) -> None:
        ax = self.figure.add_subplot(111, projection="3d")
        x1_col, x2_col = self.X_.columns[0], self.X_.columns[1]
        x1 = self.X_[x1_col].to_numpy()
        x2 = self.X_[x2_col].to_numpy()
        y_vals = self.y_.to_numpy()

        # scatter
        ax.scatter(x1, x2, y_vals, alpha=0.6, edgecolors="k",
                   linewidths=0.3, label="Data", zorder=3)

        # regression plane (grid)
        x1_grid = np.linspace(x1.min(), x1.max(), 30)
        x2_grid = np.linspace(x2.min(), x2.max(), 30)
        X1, X2 = np.meshgrid(x1_grid, x2_grid)
        grid_df = pd.DataFrame({x1_col: X1.ravel(), x2_col: X2.ravel()})
        Z = self.predict_fn(grid_df).to_numpy().reshape(X1.shape)

        ax.plot_surface(X1, X2, Z, alpha=0.35, color="crimson",
                        edgecolor="none", label="Regression plane")

        ax.set_xlabel(x1_col)
        ax.set_ylabel(x2_col)
        ax.set_zlabel(self.y_.name or "y")
        ax.set_title(f"{self.y_.name or 'y'}  ~  {x1_col}, {x2_col}")
        ax.grid(True, linestyle="--", alpha=0.3)