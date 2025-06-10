from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QPushButton, QSpinBox, QComboBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit
from models.stat_distributions import registered_distributions
from utils.constants import DEFAULT_SAMPLE_SIZES

class SimulationTab(QWidget):
    """
    A QWidget tab that allows users to run statistical simulations using various 
    parametric distributions.
    """

    def __init__(self, window, simulation_controller):
        """
        Initialize the simulation tab with required services.
        
        :param window: The parent widget that contains this tab
        :param simulation_controller: Controller for performing statistical simulations
        """
        super().__init__()
        self.window = window
        self.simulation_controller = simulation_controller
        self._init_ui()
        self._update_param_placeholder()

    def _init_ui(self):
        """Initializes and lays out all widgets in the tab."""
        layout = QVBoxLayout()
        
        self._init_distribution_controls(layout)
        self._init_parameter_controls(layout)
        self._init_alpha_controls(layout)
        self._init_save_controls(layout)
        self._init_simulation_controls(layout)
        self._init_results_t_table(layout)
        
        self.setLayout(layout)

    def _init_distribution_controls(self, layout):
        """Initialize distribution selection controls."""
        layout.addWidget(QLabel("Select Distribution:"))
        self.dist_combo = QComboBox()
        self.dist_combo.addItems(registered_distributions.keys())
        self.dist_combo.currentTextChanged.connect(self._update_param_placeholder)
        layout.addWidget(self.dist_combo)

    def _init_parameter_controls(self, layout):
        """Initialize distribution parameter controls."""
        param_layout = QHBoxLayout()
        param_label = QLabel("Distribution Parameters:")
        self.param_input = QLineEdit()
        self.param_input.setMinimumWidth(200)
        self.param_input.setPlaceholderText("x, ...")
        param_layout.addWidget(param_label)
        param_layout.addWidget(self.param_input)
        param_layout.addStretch()
        layout.addLayout(param_layout)

    def _init_alpha_controls(self, layout):
        """Initialize significance level controls."""
        alpha_layout = QHBoxLayout()
        alpha_label = QLabel("Significance Level α:")
        self.alpha_input = QLineEdit()
        self.alpha_input.setText("0.05")
        self.alpha_input.setMaximumWidth(100)
        alpha_layout.addWidget(alpha_label)
        alpha_layout.addWidget(self.alpha_input)
        alpha_layout.addStretch()
        layout.addLayout(alpha_layout)

    def _init_save_controls(self, layout):
        """Initialize data saving controls."""
        save_size_layout = QHBoxLayout()
        self.save_data_checkbox = QCheckBox("Save simulated data with size:")
        self.save_data_checkbox.setChecked(False)
        self.size_spin = QSpinBox()
        self.size_spin.setRange(10, 10000)
        self.size_spin.setValue(1000)
        self.size_spin.setMaximumWidth(150)
        save_size_layout.addWidget(self.save_data_checkbox)
        save_size_layout.addWidget(self.size_spin)
        save_size_layout.addStretch()
        layout.addLayout(save_size_layout)

    def _init_simulation_controls(self, layout):
        """Initialize simulation execution controls."""
        control_layout = QHBoxLayout()
        self.repeat_spin = QSpinBox()
        self.repeat_spin.setRange(1, 1000)
        self.repeat_spin.setValue(200)
        self.repeat_spin.setMaximumWidth(100)
        self.run_button = QPushButton("Run Simulation")
        self.run_button.clicked.connect(self.run_simulation)
        control_layout.addWidget(QLabel("Repeats:"))
        control_layout.addWidget(self.repeat_spin)
        control_layout.addWidget(self.run_button)
        control_layout.addStretch()
        layout.addLayout(control_layout)

    def _init_results_t_table(self, layout):
        """Initialize results table."""
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels([
            "Size", "T Mean", "T Std", "T Critical",
            "Params Mean", "Params Var"
        ])
        layout.addWidget(self.result_table)

    def run_simulation(self):
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
        sample_size = self.size_spin.value()

        # Create distribution instance
        dist_class = registered_distributions.get(dist_name)
        if not dist_class:
            self.window.show_error_message("Unsupported", f"Distribution {dist_name} is not supported.")
            return

        dist = dist_class()
        dist.params = params
        true_mean = dist.get_mean()
        if true_mean is None:
            self.window.show_error_message("Invalid Parameters", "Could not determine true mean from parameters.")
            return
        
        save_data = self.save_data_checkbox.isChecked()
        results = self.simulation_controller.run_simulation(
            dist, DEFAULT_SAMPLE_SIZES, repeats, true_mean, alpha, 
            save_data=save_data, sample_size=sample_size
        )
        self._populate_table(results)

    def _parse_params(self, params_str):
        try:
            params = tuple(map(float, params_str.split(',')))
            return params
        except:
            self.window.show_error_message("Invalid Parameters", "Parameters must be comma-separated numbers.")
            return
        
    def _parse_alpha(self):
        try:
            alpha = float(self.alpha_input.text())
            if not (0 < alpha < 1):
                raise ValueError
            return alpha
        except ValueError:
            self.window.show_error_message("Invalid α", "Significance level α must be between 0 and 1.")
            return

    def _populate_table(self, results):
        """
        Populate the result table with simulation results.
        :param results: List of dictionaries containing simulation results
        """
        self.result_table.setRowCount(len(results))
        for i, res in enumerate(results):
                self.result_table.setItem(i, 0, QTableWidgetItem(str(res['size'])))
                self.result_table.setItem(i, 1, QTableWidgetItem(f"{res['t_mean']:.4f}"))
                self.result_table.setItem(i, 2, QTableWidgetItem(f"{res['t_std']:.4f}"))
                self.result_table.setItem(i, 3, QTableWidgetItem(f"{res['t_crit']:.4f}"))
                self.result_table.setItem(i, 4, QTableWidgetItem(f"({', '.join(f'{x:.4f}' for x in res['params_mean'])})"))
                self.result_table.setItem(i, 5, QTableWidgetItem(f"({', '.join(f'{x:.4f}' for x in res['params_var'])})"))
         
    def _update_param_placeholder(self):
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