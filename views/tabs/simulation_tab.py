from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpinBox, QComboBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit
from services.simulation.simulation_engine import SimulationService
from models.stat_distributions import registered_distributions

class SimulationTab(QWidget):
    """
    A QWidget tab that allows users to run statistical simulations using various 
    parametric distributions.
    """

    def __init__(self, window):
        super().__init__()
        self.window = window
        self._init_ui()

    def _init_ui(self):
        """
        Initializes and lays out all widgets in the tab.
        """
        layout = QVBoxLayout()

        # Dropdown for choosing distribution
        self.dist_combo = QComboBox()
        self.dist_combo.addItems(registered_distributions.keys())

        # Input layout for parameters and significance level
        param_layout = QHBoxLayout()
        param_label = QLabel("Distribution Parameters:")
        self.param_input = QLineEdit()
        self.param_input.setPlaceholderText("x, ...")
        alpha_label = QLabel("Significance Level α:")
        self.alpha_input = QLineEdit()
        self.alpha_input.setText("0.05")

        param_layout.addWidget(param_label)
        param_layout.addWidget(self.param_input)
        param_layout.addWidget(alpha_label)
        param_layout.addWidget(self.alpha_input)

        # Control layout for repeat count and run button
        control_layout = QHBoxLayout()
        self.repeat_spin = QSpinBox()
        self.repeat_spin.setRange(1, 1000)
        self.repeat_spin.setValue(200)
        self.run_button = QPushButton("Run Simulation")
        self.run_button.clicked.connect(self.run_simulation)

        control_layout.addWidget(QLabel("Repeats:"))
        control_layout.addWidget(self.repeat_spin)
        control_layout.addWidget(self.run_button)

        # Table to display results
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Size", "T Mean", "T Std", "T Critical"])

        # Assemble all into the layout
        layout.addWidget(QLabel("Select Distribution:"))
        layout.addWidget(self.dist_combo)
        layout.addLayout(param_layout)
        layout.addLayout(control_layout)
        layout.addWidget(self.result_table)
        self.setLayout(layout)

    def run_simulation(self):
        """
        Executes the simulation using the selected distribution and user-provided parameters.
        Runs t-tests on generated samples and updates the results table.
        """
        dist_name = self.dist_combo.currentText()
        params_str = self.param_input.text()

        # Parse and validate parameters
        try:
            params = tuple(map(float, params_str.split(',')))
        except:
            self.window.show_error_message("Invalid Parameters", "Parameters must be comma-separated numbers.")
            return

        # Parse and validate significance level
        try:
            alpha = float(self.alpha_input.text())
            if not (0 < alpha < 1):
                raise ValueError
        except ValueError:
            self.window.show_error_message("Invalid α", "Significance level α must be between 0 and 1.")
            return

        sizes = [20, 50, 100, 400, 1000, 2000, 5000]
        repeats = self.repeat_spin.value()

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

        # Run experiment and populate table
        results = SimulationService.run_experiment(dist, sizes, repeats, true_mean)
        self.result_table.setRowCount(len(results))
        for i, res in enumerate(results):
            self.result_table.setItem(i, 0, QTableWidgetItem(str(res['size'])))
            self.result_table.setItem(i, 1, QTableWidgetItem(f"{res['t_mean']:.4f}"))
            self.result_table.setItem(i, 2, QTableWidgetItem(f"{res['t_std']:.4f}"))
            self.result_table.setItem(i, 3, QTableWidgetItem(f"{res['t_crit']:.4f}"))