from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, 
    QPushButton, QSpinBox, QTableWidget, 
    QTableWidgetItem, QHBoxLayout, QLineEdit
)
from typing import Optional, Dict, Any, List

from models.stat_distributions import StatisticalDistribution
from controllers import SimulationController
from services import UIMessager

DEFAULT_SAMPLE_SIZES = [20, 50, 100, 400, 1000, 2000, 5000]
DEFAULT_ALPHA_VAL_LABEL = "0.05"
MAX_ALPHA_INPUT_WIDTH = 100
SPIN_WIDTH = 150
MIN_REPEATS, MAX_REPEATS = 1, 1000
DEFAULT_REPEATS = 200
HEADING_TITLE_SIZE = 16
MIN_PARAM_INPUT_WIDTH = 200


class ExperimentWidget(QWidget):
    """Widget for running statistical experiment."""
    def __init__(self, messanger: UIMessager, simulation_controller: SimulationController):
        super().__init__()
        self.messanger: UIMessager = messanger
        self.simulation_controller: SimulationController = simulation_controller
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize experiment UI components."""
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel(f"{HEADING_TITLE_SIZE * '='} Experiment {HEADING_TITLE_SIZE * '='}"))
        self._init_parameter_controls(layout)
        self._init_alpha_controls(layout)
        self._init_experiment_controls(layout)
        self._init_results_table(layout)
        
        self.setLayout(layout)

    def _init_parameter_controls(self, layout: QVBoxLayout) -> None:
        """Initialize distribution parameter controls."""
        param_layout = QHBoxLayout()
        param_label = QLabel("Distribution Parameters:")
        self.param_input = QLineEdit()
        self.param_input.setMinimumWidth(MIN_PARAM_INPUT_WIDTH)
        self.param_input.setPlaceholderText("x, ...")
        param_layout.addWidget(param_label)
        param_layout.addWidget(self.param_input)
        param_layout.addStretch()
        layout.addLayout(param_layout)
    
    def _init_alpha_controls(self, layout: QVBoxLayout) -> None:
        """Initialize significance level controls."""
        alpha_layout = QHBoxLayout()
        alpha_label = QLabel("Significance Level α:")
        self.alpha_input = QLineEdit()
        self.alpha_input.setText(DEFAULT_ALPHA_VAL_LABEL)
        self.alpha_input.setMaximumWidth(MAX_ALPHA_INPUT_WIDTH)
        alpha_layout.addWidget(alpha_label)
        alpha_layout.addWidget(self.alpha_input)
        alpha_layout.addStretch()
        layout.addLayout(alpha_layout)
    
    def _init_experiment_controls(self, layout: QVBoxLayout) -> None:
        """Initialize experiment execution controls."""
        control_layout = QHBoxLayout()
        self.repeat_spin = QSpinBox()
        self.repeat_spin.setRange(MIN_REPEATS, MAX_REPEATS)
        self.repeat_spin.setValue(DEFAULT_REPEATS)
        self.repeat_spin.setMaximumWidth(SPIN_WIDTH)
        self.run_button = QPushButton("Run Experiment")
        control_layout.addWidget(QLabel("Repeats:"))
        control_layout.addWidget(self.repeat_spin)
        control_layout.addWidget(self.run_button)
        control_layout.addStretch()
        layout.addLayout(control_layout)
    
    def _init_results_table(self, layout: QVBoxLayout) -> None:
        """Initialize results table."""
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels([
            "Size", "T Mean", "T Std", "T Critical",
            "Params Mean", "Params Var"
        ])
        layout.addWidget(self.result_table)

    def update_param_placeholder(self, placeholder: str) -> None:
        """Update parameter input placeholder."""
        self.param_input.setPlaceholderText(placeholder)

    def get_params(self) -> Optional[tuple]:
        """Parse and validate parameters."""
        params_str = self.param_input.text().strip()
        if not params_str:
            self.messanger.show_error("Invalid Parameters", 
                "Please enter distribution parameters.")
            return None
        try:
            params = tuple(map(float, params_str.split(',')))
            return params
        except:
            self.messanger.show_error("Invalid Parameters", 
                "Parameters must be comma-separated numbers.")
            return None
    
    def run_experiment(self, dist_cls: type[StatisticalDistribution]) -> None:
        """Execute experiment with given distribution."""
        alpha = self._parse_alpha()
        if alpha is None:
            return
        params = self.get_params()
        if params is None:
            return
        
        dist = dist_cls()
        dist.params = params
        
        if not dist.validate_params():
            self.messanger.show_error("Invalid Parameters", 
                f"Could not create Distribution {dist.name} with parameters {params}.")
            return None
        
        true_mean = dist.get_mean()
        repeats = self.repeat_spin.value()

        results = self.simulation_controller.run_experiment(
            dist, DEFAULT_SAMPLE_SIZES, repeats, true_mean, alpha
        )
        self._populate_table(results)
    
    def _parse_alpha(self) -> Optional[float]:
        """Parse and validate alpha value."""
        try:
            alpha = float(self.alpha_input.text())
            if not (0 < alpha < 1):
                raise ValueError
            return alpha
        except ValueError:
            self.messanger.show_error("Invalid α", "Significance level α must be between 0 and 1.")
            return None
    
    def _populate_table(self, results: List[Dict[str, Any]]) -> None:
        """Populate the result table with experiment results."""
        self.result_table.setRowCount(len(results))
        for i, res in enumerate(results):
            self.result_table.setItem(i, 0, QTableWidgetItem(str(res['size'])))
            self.result_table.setItem(i, 1, QTableWidgetItem(f"{res['t_mean']:.4f}"))
            self.result_table.setItem(i, 2, QTableWidgetItem(f"{res['t_std']:.4f}"))
            self.result_table.setItem(i, 3, QTableWidgetItem(f"{res['t_crit']:.4f}"))
            self.result_table.setItem(i, 4, QTableWidgetItem(f"({', '.join(f'{x:.4f}' for x in res['params_mean'])})"))
            self.result_table.setItem(i, 5, QTableWidgetItem(f"({', '.join(f'{x:.4f}' for x in res['params_var'])})"))