from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QCheckBox, QLabel, 
    QPushButton, QSpinBox, QComboBox, QTableWidget, 
    QTableWidgetItem, QHBoxLayout, QLineEdit, QScrollArea,
    QFrame
)
from typing import Optional, Tuple, Dict, Any, List

from models.stat_distributions import registered_distributions
from controllers import SimulationController
from utils import AppContext
from services import UIMessager

DEFAULT_SAMPLE_SIZES = [20, 50, 100, 400, 1000, 2000, 5000]
MIN_PARAM_INPUT_WIDTH = 200
DEFAULT_ALPHA_VAL_LABEL = "0.05"
MAX_ALPHA_INPUT_WIDTH = 100
MIN_DS_SIZE, MAX_DS_SIZE = 10, 10000
DEFAULT_DS_SIZE = 1000
SPIN_WIDTH = 150
MIN_REPEATS, MAX_REPEATS = 1, 1000
DEFAULT_REPEATS = 200
HEADING_TITLE_SIZE = 16
MAX_FEATURES = 10
CORR_AREA_SCROLL_SIZE = 500
CORR_LINE_EDIT_SIZE = 100


class SimulationTab(QWidget):
    """
    A QWidget tab that allows users to run statistical simulations using various 
    parametric distributions.
    """
    def __init__(self, context: AppContext, simulation_controller: SimulationController):
        """
        Initialize the simulation tab with required services.
        Args:
            context: AppContext with messanger service
            simulation_controller: Controller for performing statistical simulations
        """
        super().__init__()
        self.messanger: UIMessager = context.messanger
        self.simulation_controller: SimulationController = simulation_controller
        self.correlation_inputs: List[Tuple[QLabel, QLineEdit]] = []
        self._init_ui()
        self._update_param_placeholder()

    def _init_ui(self) -> None:
        """Initializes and lays out all widgets in the tab."""
        layout = QVBoxLayout()

        self._init_distribution_controls(layout)
        self._init_parameter_controls(layout)
        layout.addStretch()

        layout.addWidget(QLabel(f"{HEADING_TITLE_SIZE * '='} Simulation {HEADING_TITLE_SIZE * '='}"))
        self._init_alpha_controls(layout)
        self._init_simulation_controls(layout)
        self._init_results_t_table(layout)
        layout.addStretch()

        layout.addWidget(QLabel(f"{HEADING_TITLE_SIZE * '='} Generation {HEADING_TITLE_SIZE * '='}"))
        self._init_generation_controls(layout)
        self._init_correlation_controls(layout)
        self._init_save_layout(layout)
        layout.addStretch()
        
        self.setLayout(layout)

    def _init_distribution_controls(self, layout: QVBoxLayout) -> None:
        """Initialize distribution selection controls."""
        layout.addWidget(QLabel("Select Distribution:"))
        self.dist_combo = QComboBox()
        self.dist_combo.addItems(registered_distributions.keys())
        self.dist_combo.currentTextChanged.connect(self._update_param_placeholder)
        layout.addWidget(self.dist_combo)

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

    def _init_generation_controls(self, layout: QVBoxLayout) -> None:
        """Initialize data saving controls."""
        generation_layout = QHBoxLayout()

        self.save_data_size_label = QLabel("Generated data size:")
        self.size_spin = QSpinBox()
        self.size_spin.setRange(MIN_DS_SIZE, MAX_DS_SIZE)
        self.size_spin.setValue(DEFAULT_DS_SIZE)
        self.size_spin.setMaximumWidth(SPIN_WIDTH)

        self.n_features_label = QLabel("N-features:")
        self.n_features_spin = QSpinBox()
        self.n_features_spin.setRange(1, MAX_FEATURES)
        self.n_features_spin.setValue(1)
        self.n_features_spin.setMaximumWidth(SPIN_WIDTH)
        self.n_features_spin.valueChanged.connect(self._update_correlation_inputs)

        generation_layout.addWidget(self.save_data_size_label)
        generation_layout.addWidget(self.size_spin)
        generation_layout.addWidget(self.n_features_label)
        generation_layout.addWidget(self.n_features_spin)
        generation_layout.addStretch()
        layout.addLayout(generation_layout)

    def _init_correlation_controls(self, layout: QVBoxLayout) -> None:
        """Initialize correlation coefficient input controls."""
        self.correlation_frame = QFrame()
        self.correlation_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.correlation_frame.setVisible(False)
        
        correlation_main_layout = QVBoxLayout()
        correlation_main_layout.addWidget(QLabel("Correlation Coefficients:"))
        
        # scroll area for correlation inputs
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(CORR_AREA_SCROLL_SIZE)
        
        self.correlation_widget = QWidget()
        self.correlation_layout = QVBoxLayout()
        self.correlation_widget.setLayout(self.correlation_layout)
        scroll_area.setWidget(self.correlation_widget)
        
        correlation_main_layout.addWidget(scroll_area)
        self.correlation_frame.setLayout(correlation_main_layout)
        layout.addWidget(self.correlation_frame)

    def _update_correlation_inputs(self) -> None:
        """Update correlation input fields based on number of features."""
        n_features = self.n_features_spin.value()
        for label, line_edit in self.correlation_inputs:
            self.correlation_layout.removeWidget(label)
            self.correlation_layout.removeWidget(line_edit)
            label.deleteLater()
            line_edit.deleteLater()
        self.correlation_inputs.clear()
        
        if n_features <= 1:
            self.correlation_frame.setVisible(False)
            return
        
        self.correlation_frame.setVisible(True)
        
        # create correlation input fields for upper triangle of correlation matrix
        for i in range(n_features):
            for j in range(i + 1, n_features):
                corr_layout = QHBoxLayout()
                
                label = QLabel(f"corr{{col{i+1}, col{j+1}}}:")
                line_edit = QLineEdit()
                line_edit.setPlaceholderText("0.0")
                line_edit.setMaximumWidth(CORR_LINE_EDIT_SIZE)
                
                corr_layout.addWidget(label)
                corr_layout.addWidget(line_edit)
                corr_layout.addStretch()
                
                self.correlation_layout.addLayout(corr_layout)
                self.correlation_inputs.append((label, line_edit))

    def _init_save_layout(self, layout: QVBoxLayout) -> None:
        """Initialize data export controls."""
        save_layout = QVBoxLayout()
        self.save_button = QPushButton("Save data")
        self.save_button.clicked.connect(self.save_generated_data)
        self.export_data_checkbox = QCheckBox("Export data as csv")
        self.export_data_checkbox.setChecked(False)
        save_layout.addWidget(self.export_data_checkbox)
        save_layout.addWidget(self.save_button)
        layout.addLayout(save_layout)

    def _init_simulation_controls(self, layout: QVBoxLayout) -> None:
        """Initialize simulation execution controls."""
        control_layout = QHBoxLayout()
        self.repeat_spin = QSpinBox()
        self.repeat_spin.setRange(MIN_REPEATS, MAX_REPEATS)
        self.repeat_spin.setValue(DEFAULT_REPEATS)
        self.repeat_spin.setMaximumWidth(SPIN_WIDTH)
        self.run_button = QPushButton("Run Simulation")
        self.run_button.clicked.connect(self.run_simulation)
        control_layout.addWidget(QLabel("Repeats:"))
        control_layout.addWidget(self.repeat_spin)
        control_layout.addWidget(self.run_button)
        control_layout.addStretch()
        layout.addLayout(control_layout)

    def _init_results_t_table(self, layout: QVBoxLayout) -> None:
        """Initialize results table."""
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels([
            "Size", "T Mean", "T Std", "T Critical",
            "Params Mean", "Params Var"
        ])
        layout.addWidget(self.result_table)

    def run_simulation(self) -> None:
        """
        Executes the simulation using the selected distribution and user-provided parameters.
        Runs t-tests on generated samples and updates the results table.
        """
        dist_name = self.dist_combo.currentText()
        params_str = self.param_input.text()

        # parse inputs
        params = self._parse_params(params_str)
        alpha = self._parse_alpha()
        repeats = self.repeat_spin.value()

        # сreate distribution instance
        dist_class = registered_distributions.get(dist_name)
        if not dist_class:
            self.messanger.show_error("Unsupported", f"Distribution {dist_name} is not supported.")
            return
        dist = dist_class()
        dist.params = params
        if not dist.validate_params():
            self.messanger.show_error("Invalid Parameters", f"Could not create Distribution {dist_name} with parameters {params}.")
            return            
        true_mean = dist.get_mean()
        if true_mean is None:
            self.messanger.show_error("Invalid Parameters", "Could not determine true mean from parameters.")
            return
        results = self.simulation_controller.run_simulation(
            dist, DEFAULT_SAMPLE_SIZES, repeats, true_mean, alpha, 
        )
        self._populate_table(results)

    def save_generated_data(self) -> None:
        """
        Executes the data generation using the selected distribution and user-provided parameters.
        Saves generated data and optionally exports it.
        """
        dist_name = self.dist_combo.currentText()
        params_str = self.param_input.text()
        
        # parse inputs
        params = self._parse_params(params_str)
        if params is None:
            return
        # Create distribution instance
        dist_class = registered_distributions.get(dist_name)
        if not dist_class:
            self.messanger.show_error("Unsupported", f"Distribution {dist_name} is not supported.")
            return
        dist = dist_class()
        dist.params = params
        if not dist.validate_params():
            self.messanger.show_error("Invalid Parameters", 
                f"Could not create Distribution {dist_name} with parameters {params}.")
            return
        
        # generation parameters
        n_features = self.n_features_spin.value()
        sample_size = self.size_spin.value()
        export_data = self.export_data_checkbox.isChecked()
        
        # correlation matrix
        corr_matrix = None
        if n_features > 1:
            corr_matrix = self.get_correlation_matrix()
            if corr_matrix is None:
                return
        
        # generate data
        self.simulation_controller.generate_data(
            dist, n_features, corr_matrix, sample_size, export_data
        )

    def get_correlation_matrix(self) -> Optional[List[List[float]]]:
        """
        Parse correlation coefficients from input fields and construct correlation matrix.
        Returns:
            Correlation matrix as list of lists, or None if parsing fails
        """
        n_features = self.n_features_spin.value()
        if n_features <= 1: return None
        
        # init correlation matrix
        corr_matrix = [[1.0 if i == j else 0.0 for j in range(n_features)] for i in range(n_features)]
        
        input_idx = 0
        for i in range(n_features):
            for j in range(i + 1, n_features):
                if input_idx >= len(self.correlation_inputs):
                    break
                
                _, line_edit = self.correlation_inputs[input_idx]
                text = line_edit.text().strip()
                
                try:
                    if text:
                        corr_value = float(text)
                        if not (-1 <= corr_value <= 1):
                            self.messanger.show_error("Invalid Correlation", 
                                f"Correlation corr{{col{i+1}, col{j+1}}} must be between -1 and 1.")
                            return None
                        corr_matrix[i][j] = corr_value
                        corr_matrix[j][i] = corr_value
                    else:
                        # default to 0 if empty
                        corr_matrix[i][j] = 0.0
                        corr_matrix[j][i] = 0.0
                except ValueError:
                    self.messanger.show_error("Invalid Correlation", 
                        f"Correlation corr{{col{i+1}, col{j+1}}} must be a number.")
                    return None
                
                input_idx += 1
        
        return corr_matrix

    def _parse_params(self, params_str) -> Optional[Tuple[float]]:
        try:
            params = tuple(map(float, params_str.split(',')))
            return params
        except:
            self.messanger.show_error("Invalid Parameters", "Parameters must be comma-separated numbers.")
            return
        
    def _parse_alpha(self) -> Optional[float]:
        try:
            alpha = float(self.alpha_input.text())
            if not (0 < alpha < 1):
                raise ValueError
            return alpha
        except ValueError:
            self.messanger.show_error("Invalid α", "Significance level α must be between 0 and 1.")
            return

    def _populate_table(self, results: Dict[str, Any]) -> None:
        """
        Populate the result table with simulation results.
        Args:
            results: List of dictionaries containing simulation results
        """
        self.result_table.setRowCount(len(results))
        for i, res in enumerate(results):
                self.result_table.setItem(i, 0, QTableWidgetItem(str(res['size'])))
                self.result_table.setItem(i, 1, QTableWidgetItem(f"{res['t_mean']:.4f}"))
                self.result_table.setItem(i, 2, QTableWidgetItem(f"{res['t_std']:.4f}"))
                self.result_table.setItem(i, 3, QTableWidgetItem(f"{res['t_crit']:.4f}"))
                self.result_table.setItem(i, 4, QTableWidgetItem(f"({', '.join(f'{x:.4f}' for x in res['params_mean'])})"))
                self.result_table.setItem(i, 5, QTableWidgetItem(f"({', '.join(f'{x:.4f}' for x in res['params_var'])})"))
         
    def _update_param_placeholder(self) -> None:
            """
            Update the placeholder text for param_input based on the selected distribution.
            """
            dist_name = self.dist_combo.currentText()
            dist_class = registered_distributions.get(dist_name)
            if dist_class:
                dist_instance = dist_class()
                params = dist_instance.distribution_params
                param_names = ", ".join([key for key, value in params.items()])
                self.param_input.setPlaceholderText(param_names)
            else:
                self.param_input.setPlaceholderText("x, ...")