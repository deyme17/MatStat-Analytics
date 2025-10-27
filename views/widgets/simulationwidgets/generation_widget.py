from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QCheckBox, QLabel, QPushButton, QSpinBox, 
    QHBoxLayout, QLineEdit, QScrollArea, QFrame
)
from typing import Optional, Tuple, List

from controllers import SimulationController
from services import UIMessager

MIN_DS_SIZE, MAX_DS_SIZE = 10, 10000
DEFAULT_DS_SIZE = 1000
SPIN_WIDTH = 150
HEADING_TITLE_SIZE = 16
MAX_FEATURES = 10
CORR_AREA_SCROLL_SIZE = 500
CORR_LINE_EDIT_SIZE = 100


class GenerationWidget(QWidget):
    """Widget for generating and saving data from distributions."""
    def __init__(self, messanger: UIMessager, simulation_controller: SimulationController):
        super().__init__()
        self.messanger = messanger
        self.simulation_controller = simulation_controller
        self.correlation_inputs: List[Tuple[QLabel, QLineEdit]] = []
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize generation UI components."""
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel(f"{HEADING_TITLE_SIZE * '='} Generation {HEADING_TITLE_SIZE * '='}"))
        self._init_generation_controls(layout)
        self._init_correlation_controls(layout)
        self._init_save_layout(layout)
        
        self.setLayout(layout)
    
    def _init_generation_controls(self, layout: QVBoxLayout) -> None:
        """Initialize data generation controls."""
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
        self.export_data_checkbox = QCheckBox("Export data as csv")
        self.export_data_checkbox.setChecked(False)
        save_layout.addWidget(self.export_data_checkbox)
        save_layout.addWidget(self.save_button)
        layout.addLayout(save_layout)
    
    def save_generated_data(self, dist) -> None:
        """Generate and save data from distribution."""
        if not dist.validate_params():
            self.messanger.show_error("Invalid Parameters", 
                f"Could not create Distribution {dist.name} with parameters {dist.params}.")
            return
        
        n_features = self.n_features_spin.value()
        sample_size = self.size_spin.value()
        export_data = self.export_data_checkbox.isChecked()
        
        corr_matrix = None
        if n_features > 1:
            corr_matrix = self.get_correlation_matrix()
            if corr_matrix is None:
                return
        
        self.simulation_controller.generate_data(
            dist, n_features, corr_matrix, sample_size, export_data
        )
    
    def get_correlation_matrix(self) -> Optional[List[List[float]]]:
        """Parse correlation coefficients and construct correlation matrix."""
        n_features = self.n_features_spin.value()
        if n_features <= 1:
            return None
        
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
                        corr_matrix[i][j] = 0.0
                        corr_matrix[j][i] = 0.0
                except ValueError:
                    self.messanger.show_error("Invalid Correlation", 
                        f"Correlation corr{{col{i+1}, col{j+1}}} must be a number.")
                    return None
                
                input_idx += 1
        
        return corr_matrix