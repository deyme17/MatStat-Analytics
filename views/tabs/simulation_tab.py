from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, 
)

from controllers import SimulationController, DistributionRegister
from views.widgets.simulationwidgets import ExperimentWidget, GenerationWidget
from services import UIMessager


class SimulationTab(QWidget):
    """Main tab that combines experiment and generation widgets."""
    def __init__(self, messanger: UIMessager, simulation_controller: SimulationController, 
                 dist_register: DistributionRegister, experiment_widget: type[ExperimentWidget], 
                 generation_widget: type[GenerationWidget]):
        super().__init__()
        self.messanger: UIMessager = messanger
        self.simulation_controller: SimulationController = simulation_controller
        self.dist_register: DistributionRegister = dist_register
        self.experiment_widget: ExperimentWidget = experiment_widget(messanger, simulation_controller)
        self.generation_widget: GenerationWidget = generation_widget(messanger, simulation_controller)
        self._init_ui()
        self._update_param_placeholders()
    
    def _init_ui(self) -> None:
        """Initialize the main tab layout."""
        layout = QVBoxLayout()
        
        # dist selection
        self._init_distribution_controls(layout)
        
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
        self.dist_combo.addItems(self.dist_register.distributions)
        self.dist_combo.currentTextChanged.connect(self._update_param_placeholders)
        layout.addWidget(self.dist_combo)
    
    def _update_param_placeholders(self) -> None:
        """Update parameter input placeholders in both widgets."""
        dist_name = self.dist_combo.currentText()
        dist_class = self.dist_register.get_dist(dist_name)
        if dist_class:
            dist_instance = dist_class()
            params = dist_instance.distribution_params
            param_names = ", ".join([key for key in params.keys()])
            self.experiment_widget.update_param_placeholder(param_names)
            self.generation_widget.update_param_placeholder(param_names)
        else:
            self.experiment_widget.update_param_placeholder("x, ...")
            self.generation_widget.update_param_placeholder("x, ...")
    
    def run_experiment(self) -> None:
        """Execute experiment with selected distribution."""
        dist_name = self.dist_combo.currentText()
        dist_cls = self.dist_register.get_dist(dist_name)
        if not dist_cls:
            self.messanger.show_error("Unsupported", 
                f"Distribution {dist_name} is not supported.")
            return None
        self.experiment_widget.run_experiment(dist_cls)
    
    def save_generated_data(self) -> None:
        """Generate and save data with selected distribution."""
        dist_name = self.dist_combo.currentText()
        dist_cls = self.dist_register.get_dist(dist_name)
        if not dist_cls:
            self.messanger.show_error("Unsupported", 
                f"Distribution {dist_name} is not supported.")
            return None
        self.generation_widget.save_generated_data(dist_cls)