from typing import Any, Callable
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidgetItem
from models.stat_distributions import BaseDistribution
from controllers import SimulationController
from services import UIMessager
from utils.ui_styles import groupMargin, groupStyle
from views.widgets.utils import (
    create_section_header, make_button, create_styled_result_table, fit_table_height
)
from views.widgets.simulationwidgets.subwidgets import ExperimentConfigWidget

DEFAULT_SAMPLE_SIZES = [20, 50, 100, 400, 1000, 2000, 5000]
MAX_RESULT_TABLE_HEIGHT = 400


class ExperimentWidget(QWidget):
    """Widget for running statistical experiments on distributions."""
    def __init__(self, messanger: UIMessager, simulation_controller: SimulationController):
        super().__init__()
        self.messanger: UIMessager = messanger
        self.simulation_controller: SimulationController = simulation_controller
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize experiment UI components."""
        self.setStyleSheet(groupStyle + groupMargin)
        layout = QVBoxLayout(self)

        layout.addLayout(create_section_header("Experiment"))

        self.config_widget = ExperimentConfigWidget()
        layout.addWidget(self.config_widget)

        self._init_results_table(layout)

    def _init_results_table(self, layout: QVBoxLayout) -> None:
        """Initialize styled results table."""
        self.result_table = create_styled_result_table()
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels([
            "Size", "T Mean", "T Std", "T Critical",
            "Params Mean", "Params Var"
        ])
        layout.addWidget(self.result_table)

    def update_param_placeholder(self, placeholder: str) -> None:
        """Update parameter input placeholder in subwidget."""
        self.config_widget.set_placeholder(placeholder)

    def run_experiment(self, dist_cls: type[BaseDistribution]) -> None:
        """Execute experiment with given distribution."""
        alpha = self.config_widget.get_alpha()
        params = self.config_widget.parse_params(self.messanger)
        if params is None:
            return

        dist = dist_cls()
        dist.params = params

        if not dist.validate_params():
            self.messanger.show_error(
                "Invalid Parameters", 
                f"Could not create Distribution {dist.name} with parameters {params}."
            )
            return

        true_mean = dist.get_mean()
        repeats = self.config_widget.get_repeats()

        results = self.simulation_controller.run_experiment(
            dist, DEFAULT_SAMPLE_SIZES, repeats, true_mean, alpha
        )
        self._populate_table(results)

    def _populate_table(self, results: list[dict[str, Any]]) -> None:
        """Populate the result table with experiment results."""
        self.result_table.setRowCount(len(results))
        for i, res in enumerate(results):
            self.result_table.setItem(i, 0, QTableWidgetItem(str(res['size'])))
            self.result_table.setItem(i, 1, QTableWidgetItem(f"{res['t_mean']:.4f}"))
            self.result_table.setItem(i, 2, QTableWidgetItem(f"{res['t_std']:.4f}"))
            self.result_table.setItem(i, 3, QTableWidgetItem(f"{res['t_crit']:.4f}"))
            self.result_table.setItem(i, 4, QTableWidgetItem(f"({', '.join(f'{x:.4f}' for x in res['params_mean'])})"))
            self.result_table.setItem(i, 5, QTableWidgetItem(f"({', '.join(f'{x:.4f}' for x in res['params_var'])})"))

        self.result_table.resizeColumnsToContents()
        fit_table_height(self.result_table)

    def set_on_run_callback(self, callback: Callable[[], None]) -> None:
        """Set callback for run experiment button click."""
        self.config_widget.run_button.clicked.connect(callback)