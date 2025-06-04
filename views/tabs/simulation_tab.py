from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QPushButton, QSpinBox, QComboBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit
from services.simulation.simulation_engine import SimulationService
from models.stat_distributions import registered_distributions
from models.data_model import DataModel

import pandas as pd
import numpy as np

class SimulationTab(QWidget):
    """
    A QWidget tab that allows users to run statistical simulations using various 
    parametric distributions.
    """

    def __init__(self, window):
        super().__init__()
        self.window = window
        self._init_ui()
        self.simulation_counter = {}
        self._update_param_placeholder()

    def _init_ui(self):
        """
        Initializes and lays out all widgets in the tab.
        """
        layout = QVBoxLayout()

        # dropdown for choosing dist
        self.dist_combo = QComboBox()
        self.dist_combo.addItems(registered_distributions.keys())
        self.dist_combo.currentTextChanged.connect(self._update_param_placeholder)

        # dist parameters
        param_layout = QHBoxLayout()
        param_label = QLabel("Distribution Parameters:")
        self.param_input = QLineEdit()
        self.param_input.setMinimumWidth(200)
        self.param_input.setPlaceholderText("x, ...")
        param_layout.addWidget(param_label)
        param_layout.addWidget(self.param_input)
        param_layout.addStretch() 

        # significance level
        alpha_layout = QHBoxLayout()
        alpha_label = QLabel("Significance Level α:")
        self.alpha_input = QLineEdit()
        self.alpha_input.setText("0.05")
        self.alpha_input.setMaximumWidth(100)
        alpha_layout.addWidget(alpha_label)
        alpha_layout.addWidget(self.alpha_input)
        alpha_layout.addStretch()

        # save checkbox and sample size
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

        # repeat count and run button
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

        # results
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Size", "T Mean", "T Std", "T Critical"])

        # layout
        layout.addWidget(QLabel("Select Distribution:"))
        layout.addWidget(self.dist_combo)
        layout.addLayout(param_layout)
        layout.addLayout(alpha_layout)
        layout.addLayout(save_size_layout)
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
        
        if self.save_data_checkbox.isChecked():
            simulated_data = SimulationService.generate_sample(dist, sample_size, params)
            self._save_simulated_data(dist_name, simulated_data, params)

        # Run experiment and populate table
        results = SimulationService.run_experiment(dist, sizes, repeats, true_mean)
        self.result_table.setRowCount(len(results))
        for i, res in enumerate(results):
            self.result_table.setItem(i, 0, QTableWidgetItem(str(res['size'])))
            self.result_table.setItem(i, 1, QTableWidgetItem(f"{res['t_mean']:.4f}"))
            self.result_table.setItem(i, 2, QTableWidgetItem(f"{res['t_std']:.4f}"))
            self.result_table.setItem(i, 3, QTableWidgetItem(f"{res['t_crit']:.4f}"))

    def _save_simulated_data(self, dist_name: str, data: np.ndarray, params: tuple):
        """
        Save simulated data as a new dataset in the data history manager.
        
        :param dist_name: name of the distribution
        :param data: simulated data array
        :param params: distribution parameters
        """
        if dist_name not in self.simulation_counter:
            self.simulation_counter[dist_name] = 0
        
        self.simulation_counter[dist_name] += 1
        counter = self.simulation_counter[dist_name]
        
        # dataset label
        dataset_label = f"{dist_name}Simulation{counter}"
        series = pd.Series(data)
        
        # bin count
        from utils.def_bins import get_default_bin_count
        optimal_bins = get_default_bin_count(series)
        
        # DataModel
        data_model = DataModel(series, bins=optimal_bins, label=dataset_label)

        self.window.version_manager.add_dataset(dataset_label, data_model)
        self.window.data_model = data_model
        
        # Postprocess loaded data to update UI
        from services.data_services.data_loader_service import DataLoaderService
        DataLoaderService.postprocess_loaded_data(self.window, series)
        
        # Show success message
        self.window.show_info_message(
            "Data Saved", 
            f"Simulated data saved as '{dataset_label}' with {len(data)} samples."
        )

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