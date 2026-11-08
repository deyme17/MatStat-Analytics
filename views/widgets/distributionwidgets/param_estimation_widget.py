from typing import Callable
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QComboBox, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem
)
from utils import AppContext
from services import UIMessager
from controllers import EstimationController
from models.stat_distributions import BaseDistribution

MIN_TABLE_HEIGHT = 100


class ParamEstimationWidget(QWidget):
    """Estimates distribution parameters using the selected method."""
    def __init__(self, context: AppContext, 
                 estimator: EstimationController,
                 get_dist_func: Callable[[], BaseDistribution | None] | None = None) -> None:
        super().__init__()
        self.context = context
        self.messanger: UIMessager = context.messanger
        self.estimator = estimator
        self.get_dist_func = get_dist_func
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.method_combo = QComboBox()
        self.method_combo.addItems(self.estimator.methods)

        self.estimate_button = QPushButton("Estimate Parameters")
        self.estimate_button.clicked.connect(self._handle_estimation)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(2)
        self.result_table.setHorizontalHeaderLabels(["Parameter", "Estimated Value"])
        self.result_table.setMinimumHeight(MIN_TABLE_HEIGHT)

        layout.addWidget(QLabel("Select Estimation Method:"))
        layout.addWidget(self.method_combo)
        layout.addWidget(self.estimate_button)
        layout.addWidget(self.result_table)

    def _handle_estimation(self) -> None:
        if self.get_dist_func is None:
            raise RuntimeError("No distribution access. Call `set_distribution_access` first.")
        if not self.context.data_model or not self.messanger:
            return

        data = self.context.data_model.series
        if data is None:
            self.messanger.show_error("No Data", "No data available for estimation")
            return
        if data.empty or data.isna().all():
            self.messanger.show_error("Invalid Data", "Data contains no valid values")
            return

        dist = self.get_dist_func()
        if dist is None:
            self.messanger.show_error("Invalid Distribution", "No valid distribution selected")
            return

        dist_name = type(dist).__name__
        try:
            params = self.estimator.estimate(dist, self.method_combo.currentText(), data)
            if params is None:
                self.messanger.show_error(
                    "Estimation Failed", f"Failed to estimate parameters for {dist_name}")
                return
            self._display_results(dist, params)
        except Exception as e:
            self.messanger.show_error("Estimation Error", f"Error during estimation: {e}")

    def _display_results(self, distribution: BaseDistribution, params: list) -> None:
        param_names = list(distribution.distribution_params.keys())
        self.result_table.setRowCount(len(params))
        for i, (name, value) in enumerate(zip(param_names, params)):
            self.result_table.setItem(i, 0, QTableWidgetItem(name))
            self.result_table.setItem(i, 1, QTableWidgetItem(f"{value:.4f}"))

    def clear_results(self) -> None:
        self.result_table.setRowCount(0)

    def set_distribution_access(self, get_dist_func: Callable[[], BaseDistribution]) -> None:
        self.get_dist_func = get_dist_func