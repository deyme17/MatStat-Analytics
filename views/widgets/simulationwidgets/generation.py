from typing import Callable
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QHBoxLayout
from models.stat_distributions import BaseDistribution
from controllers import SimulationController
from services import UIMessager
from utils.ui_styles import groupMargin, groupStyle
from views.widgets.utils import create_section_header, make_button, make_checkbox
from views.widgets.simulationwidgets.subwidgets import GenerationParamsWidget

MIN_DS_SIZE, MAX_DS_SIZE = 10, 10000
DEFAULT_DS_SIZE = 1000
SPIN_WIDTH = 150
MAX_FEATURES = 9


class GenerationWidget(QWidget):
    """Widget for generating and saving data from statistical distributions."""
    def __init__(self, messanger: UIMessager, simulation_controller: SimulationController):
        super().__init__()
        self.messanger: UIMessager = messanger
        self.simulation_controller: SimulationController = simulation_controller
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize generation UI components."""
        self.setStyleSheet(groupStyle + groupMargin)
        layout = QVBoxLayout(self)

        layout.addLayout(create_section_header("Generation"))
        self._init_generation_controls(layout)

        self.params_widget = GenerationParamsWidget()
        layout.addWidget(self.params_widget)
        self.params_widget.update_fields(self.n_features_spin.value())

        self._init_save_layout(layout)

    def _init_generation_controls(self, layout: QVBoxLayout) -> None:
        """Initialize size and feature count controls."""
        gen_layout = QHBoxLayout()

        self.size_spin = QSpinBox()
        self.size_spin.setRange(MIN_DS_SIZE, MAX_DS_SIZE)
        self.size_spin.setValue(DEFAULT_DS_SIZE)
        self.size_spin.setMaximumWidth(SPIN_WIDTH)

        self.n_features_spin = QSpinBox()
        self.n_features_spin.setRange(1, MAX_FEATURES)
        self.n_features_spin.setValue(1)
        self.n_features_spin.setMaximumWidth(SPIN_WIDTH)
        self.n_features_spin.valueChanged.connect(self._on_features_count_changed)

        gen_layout.addWidget(QLabel("Generated data size:"))
        gen_layout.addWidget(self.size_spin)
        gen_layout.addWidget(QLabel("N-features:"))
        gen_layout.addWidget(self.n_features_spin)
        gen_layout.addStretch()

        layout.addLayout(gen_layout)

    def _init_save_layout(self, layout: QVBoxLayout) -> None:
        """Initialize data export controls."""
        save_layout = QVBoxLayout()
        self.export_data_checkbox = make_checkbox("Export data as csv", checked=False)
        self.save_button = make_button("Save data", callback=None, height=32)

        save_layout.addWidget(self.export_data_checkbox)
        save_layout.addWidget(self.save_button)
        layout.addLayout(save_layout)

    def _on_features_count_changed(self, value: int) -> None:
        """Update parameter inputs based on feature count."""
        self.params_widget.update_fields(value)

    def update_param_placeholder(self, placeholder: str) -> None:
        """Update placeholder in subwidget."""
        self.params_widget.update_placeholder(placeholder)

    def save_generated_data(self, dist_cls: type[BaseDistribution]) -> None:
        """Generate and save dataset using specified distribution."""
        n_features = self.n_features_spin.value()
        sample_size = self.size_spin.value()
        export_data = self.export_data_checkbox.isChecked()
        
        params_list = self.params_widget.parse_params(self.messanger)
        if params_list is None:
            return

        corr_matrix = self.params_widget.parse_correlation_matrix(n_features, self.messanger) if n_features > 1 else None
        if n_features > 1 and corr_matrix is None:
            return

        self.simulation_controller.generate_data(
            dist_cls(), n_features, params_list, corr_matrix, sample_size, export_data,
        )

    def set_on_save_callback(self, callback: Callable[[], None]) -> None:
        """Set callback for save data button click."""
        self.save_button.clicked.connect(callback)