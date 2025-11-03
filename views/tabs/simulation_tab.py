from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, 
    QHBoxLayout, QLineEdit
)
from typing import Optional, Tuple

from models.stat_distributions import registered_distributions
from controllers import SimulationController
from views.widgets.simulationwidgets import ExperimentWidget, GenerationWidget
from services import UIMessager

MIN_PARAM_INPUT_WIDTH = 200


class SimulationTab(QWidget):
    """Main tab that combines experiment and generation widgets."""
    def __init__(self, messanger: UIMessager, simulation_controller: SimulationController,
                 experiment_widget: type[ExperimentWidget], generation_widget: type[GenerationWidget]):
        super().__init__()
        self.messanger: UIMessager = messanger
        self.simulation_controller: SimulationController = simulation_controller
        self.experiment_widget: ExperimentWidget = experiment_widget(messanger, simulation_controller)
        self.generation_widget: GenerationWidget = generation_widget(messanger, simulation_controller)
        self._init_ui()
        self._update_param_placeholder()
    
    def _init_ui(self) -> None:
        """Initialize the main tab layout."""
        layout = QVBoxLayout()
        
        # dist selection
        self._init_distribution_controls(layout)
        self._init_parameter_controls(layout)
        
        # generation widget
        layout.addWidget(self.generation_widget)
        self.generation_widget.save_button.clicked.connect(self.save_generated_data)
        
        # experiment widget
        layout.addWidget(self.experiment_widget)
        self.experiment_widget.run_button.clicked.connect(self.run_experiment)
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
    
    def run_experiment(self) -> None:
        """Execute experiment with selected distribution."""
        dist = self._create_distribution()
        if dist is None:
            return
        
        true_mean = dist.get_mean()
        if true_mean is None:
            self.messanger.show_error("Invalid Parameters", "Could not determine true mean from parameters.")
            return
        
        self.experiment_widget.run_experiment(dist, true_mean)
    
    def save_generated_data(self) -> None:
        """Generate and save data with selected distribution."""
        dist = self._create_distribution()
        if dist is None:
            return
        
        self.generation_widget.save_generated_data(dist)
    
    def _create_distribution(self):
        """Create distribution instance from user input."""
        dist_name = self.dist_combo.currentText()
        params_str = self.param_input.text()
        
        params = self._parse_params(params_str)
        if params is None:
            return None
        
        dist_class = registered_distributions.get(dist_name)
        if not dist_class:
            self.messanger.show_error("Unsupported", f"Distribution {dist_name} is not supported.")
            return None
        
        dist = dist_class()
        dist.params = params
        
        if not dist.validate_params():
            self.messanger.show_error("Invalid Parameters", 
                f"Could not create Distribution {dist_name} with parameters {params}.")
            return None
        
        return dist
    
    def _parse_params(self, params_str: str) -> Optional[Tuple[float, ...]]:
        """Parse comma-separated parameters."""
        try:
            params = tuple(map(float, params_str.split(',')))
            return params
        except:
            self.messanger.show_error("Invalid Parameters", "Parameters must be comma-separated numbers.")
            return None
    
    def _update_param_placeholder(self) -> None:
        """Update parameter input placeholder based on selected distribution."""
        dist_name = self.dist_combo.currentText()
        dist_class = registered_distributions.get(dist_name)
        if dist_class:
            dist_instance = dist_class()
            params = dist_instance.distribution_params
            param_names = ", ".join([key for key in params.keys()])
            self.param_input.setPlaceholderText(param_names)
        else:
            self.param_input.setPlaceholderText("x, ...")