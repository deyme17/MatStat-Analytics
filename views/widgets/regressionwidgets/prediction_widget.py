from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QGroupBox, QFormLayout, QScrollArea
)
from PyQt6.QtCore import Qt
from services.ui_services.messager import UIMessager
from utils import AppContext
from controllers import RegressionController
from utils.ui_styles import groupMargin, groupStyle
import pandas as pd

HEADING_TITLE_SIZE = 13
MAX_X_INPUT_SECTION_HEIGHT = 200
DEFAULT_ALPHA = 0.05


class RegrPredictionWidget(QWidget):
    """Widget for making predictions for new data using fitted model."""
    def __init__(self, context: AppContext, regr_controller: RegressionController):
        super().__init__()
        self.context: AppContext = context
        self.messanger: UIMessager = context.messanger
        self.controller: RegressionController = regr_controller
        self.feature_inputs: dict[str, QLineEdit] = {}
        self.alpha: float = DEFAULT_ALPHA
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize regression prediction UI components."""
        self.setStyleSheet(groupStyle + groupMargin)
        layout = QVBoxLayout()
        
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel(f"{'=' * HEADING_TITLE_SIZE} Prediction Section {'=' * HEADING_TITLE_SIZE}"))
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        self._init_input_section(layout)
        
        self.predict_btn = QPushButton("Predict")
        self.predict_btn.clicked.connect(self._predict)
        layout.addWidget(self.predict_btn)
        
        self._init_result_section(layout)
        self._init_intervals_section(layout)
        self.setLayout(layout)

    def _init_input_section(self, layout: QVBoxLayout) -> None:
        """Initialize input section for feature values."""
        group = QGroupBox("Input Feature Values")
        self.form_layout = QFormLayout()
        
        self.inputs_container = QWidget()
        self.inputs_container.setLayout(self.form_layout)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.inputs_container)
        scroll.setMaximumHeight(MAX_X_INPUT_SECTION_HEIGHT)
        
        group_layout = QVBoxLayout()
        group_layout.addWidget(scroll)
        group.setLayout(group_layout)
        layout.addWidget(group)

    def _init_result_section(self, layout: QVBoxLayout) -> None:
        """Initialize result section."""
        group = QGroupBox("Prediction Result")
        group_layout = QVBoxLayout()
        
        self.result_label = QLabel("No prediction yet.")
        self.result_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        group_layout.addWidget(self.result_label)
        group.setLayout(group_layout)
        layout.addWidget(group)

    def _init_intervals_section(self, layout: QVBoxLayout) -> None:
        """Initialize intervals section for confidence and prediction intervals."""
        group = QGroupBox("Prediction Intervals")
        group_layout = QVBoxLayout()
        
        # ci
        ci_mean_layout = QHBoxLayout()
        ci_mean_layout.addWidget(QLabel("Confidence Interval (mean):"))
        self.ci_mean_label = QLabel("-")
        ci_mean_layout.addWidget(self.ci_mean_label)
        ci_mean_layout.addStretch()
        group_layout.addLayout(ci_mean_layout)

        # pi
        ci_ind_layout = QHBoxLayout()
        ci_ind_layout.addWidget(QLabel("Prediction Interval (individual):"))
        self.ci_ind_label = QLabel("-")
        ci_ind_layout.addWidget(self.ci_ind_label)
        ci_ind_layout.addStretch()
        group_layout.addLayout(ci_ind_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)

    def setup_for_model(self, feature_names: list[str]) -> None:
        """Setup input fields based on fitted model features."""
        self.feature_inputs.clear()
        while self.form_layout.rowCount() > 0:
            self.form_layout.removeRow(0)
        
        for feature in feature_names:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Enter value for {feature}")
            self.feature_inputs[feature] = line_edit
            self.form_layout.addRow(f"{feature}:", line_edit)

    def set_alpha_value(self, alpha: float) -> None:
        """Set a new alpha (sagnificsnce level) value"""
        self.alpha = alpha

    def _predict(self) -> None:
        """Execute regression model prediction and show results."""
        if not self.feature_inputs:
            self.messanger.show_info("No model", "Please fit a model first")
            return
        
        try:
            input_data = {}
            for feature, line_edit in self.feature_inputs.items():
                value_str = line_edit.text().strip()
                if not value_str:
                    self.messanger.show_error("Input error", 
                        f"Please enter a value for {feature}")
                    return
                
                try:
                    input_data[feature] = float(value_str)
                except ValueError:
                    self.messanger.show_error("Input error", 
                        f"Invalid number for {feature}: {value_str}")
                    return
            
            X_df = pd.DataFrame([input_data])
            prediction = self.controller.predict(X_df)
            predicted_value = prediction.iloc[0]
            intervals = self.controller.predict_intervals(X_df, self.alpha)
            
            # result
            self.result_label.setText(f"Predicted value: {predicted_value:.6f}")
            self.result_label.setStyleSheet("font-weight: bold; font-size: 14px; color: green;")
            # intervals
            self._display_intervals(intervals)
            
        except Exception as e:
            self.messanger.show_error("Prediction error", str(e))
            self.result_label.setText("Prediction failed")
            self.result_label.setStyleSheet("font-weight: bold; font-size: 14px; color: red;")
            self.ci_mean_label.setText("-")
            self.ci_ind_label.setText("-")

    def _display_intervals(self, intervals: dict[str, tuple[float, float]]) -> None:
        """Displays Confidance/Predictions intervals for X"""
        try:
            ci_lower, ci_upper = intervals['CI_mean']
            self.ci_mean_label.setText(f"[{ci_lower:.4f}, {ci_upper:.4f}]")
            pi_lower, pi_upper = intervals['CI_ind']
            self.ci_ind_label.setText(f"[{pi_lower:.4f}, {pi_upper:.4f}]")
        except Exception as e:
            self.ci_mean_label.setText("Not available")
            self.ci_ind_label.setText("Not available")

    def clear(self) -> None:
        """Clear all input fields and results."""
        for line_edit in self.feature_inputs.values():
            line_edit.clear()
        self.result_label.setText("No prediction yet.")
        self.result_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        # intervals
        self.ci_mean_label.setText("-")
        self.ci_ind_label.setText("-")