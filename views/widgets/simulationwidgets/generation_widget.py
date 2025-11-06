from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QCheckBox, QLabel, QPushButton, QSpinBox, 
    QHBoxLayout, QLineEdit, QScrollArea, QFrame
)
from typing import Optional, List

from controllers import SimulationController
from services import UIMessager

MIN_DS_SIZE, MAX_DS_SIZE = 10, 10000
DEFAULT_DS_SIZE = 1000
SPIN_WIDTH = 150
HEADING_TITLE_SIZE = 16
MAX_FEATURES = 10
CORR_AREA_SCROLL_SIZE = 500
CORR_LINE_EDIT_SIZE = 100
MIN_PARAM_INPUT_WIDTH = 200


class GenerationWidget(QWidget):
    """Widget for generating and saving data from distributions."""
    def __init__(self, messanger: UIMessager, simulation_controller: SimulationController):
        super().__init__()
        self.messanger = messanger
        self.simulation_controller = simulation_controller
        self.correlation_inputs: List[tuple] = []
        self.feature_param_inputs: List[QLineEdit] = []
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize generation UI components."""
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel(f"{HEADING_TITLE_SIZE * '='} Generation {HEADING_TITLE_SIZE * '='}"))
        self._init_generation_controls(layout)
        self._init_multifeature_controls(layout)
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
        self.n_features_spin.valueChanged.connect(self._update_multifeature_inputs)
        
        generation_layout.addWidget(self.save_data_size_label)
        generation_layout.addWidget(self.size_spin)
        generation_layout.addWidget(self.n_features_label)
        generation_layout.addWidget(self.n_features_spin)
        generation_layout.addStretch()
        layout.addLayout(generation_layout)
    
    def _init_multifeature_controls(self, layout: QVBoxLayout) -> None:
        """Initialize multi-feature parameter and correlation controls."""
        self.multifeature_frame = QFrame()
        self.multifeature_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.multifeature_frame.setVisible(False)
        
        multifeature_main_layout = QVBoxLayout()
        
        # params section
        multifeature_main_layout.addWidget(QLabel("Feature-specific Parameters:"))
        self.feature_params_layout = QVBoxLayout()
        multifeature_main_layout.addLayout(self.feature_params_layout)

        multifeature_main_layout.addWidget(QLabel("-" * (HEADING_TITLE_SIZE * 2)))
        
        # correlation saection
        multifeature_main_layout.addWidget(QLabel("Correlation Coefficients:"))
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(CORR_AREA_SCROLL_SIZE)
        
        self.correlation_widget = QWidget()
        self.correlation_layout = QVBoxLayout()
        self.correlation_widget.setLayout(self.correlation_layout)
        scroll_area.setWidget(self.correlation_widget)
        
        multifeature_main_layout.addWidget(scroll_area)
        self.multifeature_frame.setLayout(multifeature_main_layout)
        layout.addWidget(self.multifeature_frame)
    
    def _update_multifeature_inputs(self) -> None:
        """Update parameter and correlation input fields based on number of features."""
        n_features = self.n_features_spin.value()
        for label, line_edit in self.correlation_inputs:
            self.correlation_layout.removeWidget(label)
            self.correlation_layout.removeWidget(line_edit)
            label.deleteLater()
            line_edit.deleteLater()
        self.correlation_inputs.clear()

        while self.feature_params_layout.count():
            item = self.feature_params_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
        self.feature_param_inputs.clear()
        
        if n_features <= 1:
            self.multifeature_frame.setVisible(False)
            return
        
        self.multifeature_frame.setVisible(True)
        
        for i in range(n_features):
            param_layout = QHBoxLayout()
            label = QLabel(f"Feature {i+1} params:")
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("e.g., 0, 1")
            line_edit.setMinimumWidth(MIN_PARAM_INPUT_WIDTH)
            param_layout.addWidget(label)
            param_layout.addWidget(line_edit)
            param_layout.addStretch()
            self.feature_params_layout.addLayout(param_layout)
            self.feature_param_inputs.append(line_edit)
        
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
    
    def _clear_layout(self, layout):
        """Helper to recursively clear a layout."""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
    
    def _init_save_layout(self, layout: QVBoxLayout) -> None:
        """Initialize data export controls."""
        save_layout = QVBoxLayout()
        self.save_button = QPushButton("Save data")
        self.export_data_checkbox = QCheckBox("Export data as csv")
        self.export_data_checkbox.setChecked(False)
        save_layout.addWidget(self.export_data_checkbox)
        save_layout.addWidget(self.save_button)
        layout.addLayout(save_layout)
    
    def update_param_placeholder(self, placeholder: str) -> None:
        """Update parameter input placeholders for all feature inputs."""
        for line_edit in self.feature_param_inputs:
            line_edit.setPlaceholderText(placeholder)
    
    def get_params(self) -> Optional[List[tuple]]:
        """
        Parse feature-specific parameters.
        Returns list of parameter tuples, one per feature.
        For single feature, returns list with one tuple.
        """
        n_features = self.n_features_spin.value()
        
        if n_features <= 1:
            # Для одновимірного - параметри мають бути введені в simulation_tab
            # Тут повертаємо None, щоб simulation_tab обробив це
            self.messanger.show_error("Configuration Error", 
                "For single feature, parameters should be set in main tab.")
            return None
        
        params_list = []
        for i, line_edit in enumerate(self.feature_param_inputs):
            text = line_edit.text().strip()
            if not text:
                self.messanger.show_error("Invalid Parameters", 
                    f"Feature {i+1} parameters are required. Please enter values.")
                return None
            
            try:
                params = tuple(map(float, text.split(',')))
                params_list.append(params)
            except ValueError:
                self.messanger.show_error("Invalid Parameters", 
                    f"Feature {i+1} parameters must be comma-separated numbers.")
                return None
        
        if len(set(len(p) for p in params_list)) > 1:
            self.messanger.show_error("Invalid Parameters", 
                "All features must have the same number of parameters.")
            return None
        
        return params_list
    
    def save_generated_data(self, dist, params_list: List[tuple]) -> None:
        """Generate and save data from distribution."""
        n_features = self.n_features_spin.value()
        sample_size = self.size_spin.value()
        export_data = self.export_data_checkbox.isChecked()
        
        corr_matrix = None
        if n_features > 1:
            corr_matrix = self.get_correlation_matrix()
            if corr_matrix is None:
                return
        
        self.simulation_controller.generate_data(
            dist, n_features, corr_matrix, sample_size, export_data, params_list
        )
    
    def get_correlation_matrix(self) -> Optional[List[List[float]]]:
        """Parse correlation coefficients and construct correlation matrix."""
        n_features = self.n_features_spin.value()
        if n_features <= 1:
            return None
        
        corr_matrix = [[1.0 if i == j else 0.0 for j in range(n_features)] 
                       for i in range(n_features)]
        
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