from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel
from PyQt6.QtCore import Qt


class RegrPredictionOutputWidget(QWidget):
    """Subwidget displaying prediction scalar result and interval bounds."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """Build result and interval group boxes layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # pred result
        res_group = QGroupBox("Prediction Result")
        res_layout = QVBoxLayout(res_group)

        self.result_label = QLabel("No prediction yet.")
        self.result_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        res_layout.addWidget(self.result_label)
        layout.addWidget(res_group)

        # intervals
        int_group = QGroupBox("Prediction Intervals")
        int_layout = QVBoxLayout(int_group)

        ci_mean_layout = QHBoxLayout()
        ci_mean_layout.addWidget(QLabel("Confidence Interval (mean):"))
        self.ci_mean_label = QLabel("-")
        ci_mean_layout.addWidget(self.ci_mean_label)
        ci_mean_layout.addStretch()
        int_layout.addLayout(ci_mean_layout)

        ci_ind_layout = QHBoxLayout()
        ci_ind_layout.addWidget(QLabel("Prediction Interval (individual):"))
        self.ci_ind_label = QLabel("-")
        ci_ind_layout.addWidget(self.ci_ind_label)
        ci_ind_layout.addStretch()
        int_layout.addLayout(ci_ind_layout)

        layout.addWidget(int_group)

    def display_success(self, predicted_value: float, intervals: dict[str, tuple[float, float]]) -> None:
        """Display successful prediction value and interval bounds."""
        self.result_label.setText(f"Predicted value: {predicted_value:.6f}")
        self.result_label.setStyleSheet("font-weight: bold; font-size: 14px; color: green;")
        
        try:
            ci_lower, ci_upper = intervals['CI_mean']
            self.ci_mean_label.setText(f"[{ci_lower:.4f}, {ci_upper:.4f}]")
            pi_lower, pi_upper = intervals['CI_ind']
            self.ci_ind_label.setText(f"[{pi_lower:.4f}, {pi_upper:.4f}]")
        except Exception:
            self.ci_mean_label.setText("Not available")
            self.ci_ind_label.setText("Not available")

    def display_error(self) -> None:
        """Display failed prediction status."""
        self.result_label.setText("Prediction failed")
        self.result_label.setStyleSheet("font-weight: bold; font-size: 14px; color: red;")
        self.ci_mean_label.setText("-")
        self.ci_ind_label.setText("-")

    def clear(self) -> None:
        """Clear prediction output values."""
        self.result_label.setText("No prediction yet.")
        self.result_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.ci_mean_label.setText("-")
        self.ci_ind_label.setText("-")