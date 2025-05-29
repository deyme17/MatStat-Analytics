from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpinBox, QComboBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit
from services.simulation.simulation_service import SimulationService
from models.stat_distributions import registered_distributions

class SimulationTab(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # Dropdown
        self.dist_combo = QComboBox()
        self.dist_combo.addItems(registered_distributions.keys())

        # params
        param_layout = QHBoxLayout()
        self.param_input = QLineEdit()
        self.param_input.setPlaceholderText("Parameters (e.g. 0,1 or 2.0)")
        self.mean_input = QLineEdit()
        self.mean_input.setPlaceholderText("True Mean")
        param_layout.addWidget(self.param_input)
        param_layout.addWidget(self.mean_input)

        # repeat and run button
        control_layout = QHBoxLayout()
        self.repeat_spin = QSpinBox()
        self.repeat_spin.setRange(1, 1000)
        self.repeat_spin.setValue(200)
        self.run_button = QPushButton("Run Simulation")
        self.run_button.clicked.connect(self.run_simulation)
        control_layout.addWidget(QLabel("Repeats:"))
        control_layout.addWidget(self.repeat_spin)
        control_layout.addWidget(self.run_button)

        # table
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(["Size", "T Mean", "T Std"])

        layout.addWidget(QLabel("Select Distribution:"))
        layout.addWidget(self.dist_combo)
        layout.addLayout(param_layout)
        layout.addLayout(control_layout)
        layout.addWidget(self.result_table)
        self.setLayout(layout)

    def run_simulation(self):
        dist_name = self.dist_combo.currentText()
        params_str = self.param_input.text()
        try:
            true_mean = float(self.mean_input.text())
        except ValueError:
            self.window.show_error_message("Invalid Input", "True mean must be a number.")
            return

        try:
            params = tuple(map(float, params_str.split(',')))
        except:
            self.window.show_error_message("Invalid Parameters", "Parameters must be comma-separated numbers.")
            return

        sizes = [20, 50, 100, 400, 1000, 2000, 5000]
        repeats = self.repeat_spin.value()

        dist_class = registered_distributions.get(dist_name)
        if not dist_class:
            self.window.show_error_message("Unsupported", f"Distribution {dist_name} is not supported.")
            return

        dist = dist_class()

        results = SimulationService.run_experiment(dist, sizes, repeats, true_mean, params)
        self.result_table.setRowCount(len(results))
        for i, res in enumerate(results):
            self.result_table.setItem(i, 0, QTableWidgetItem(str(res['size'])))
            self.result_table.setItem(i, 1, QTableWidgetItem(f"{res['t_mean']:.4f}"))
            self.result_table.setItem(i, 2, QTableWidgetItem(f"{res['t_std']:.4f}"))