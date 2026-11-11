from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox
from views.widgets.utils import make_button
from views.widgets.utils.common_widgets import AlphaControlWidget

SPIN_WIDTH = 150
MIN_REPEATS, MAX_REPEATS = 1, 1000
DEFAULT_REPEATS = 200
MIN_PARAM_INPUT_WIDTH = 200


class ExperimentConfigWidget(QWidget):
    """Subwidget managing experiment setup: parameters, significance level (alpha), and repeats count."""
    def __init__(self, on_run_callback=None, parent: QWidget | None = None):
        super().__init__(parent)
        self.on_run_callback = on_run_callback
        self._init_ui()

    def _init_ui(self) -> None:
        """Build layout for experiment configuration."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # params
        param_layout = QHBoxLayout()
        self.param_input = QLineEdit()
        self.param_input.setMinimumWidth(MIN_PARAM_INPUT_WIDTH)
        self.param_input.setPlaceholderText("x, ...")
        param_layout.addWidget(QLabel("Distribution Parameters:"))
        param_layout.addWidget(self.param_input)
        param_layout.addStretch()
        layout.addLayout(param_layout)

        # alpha
        self.alpha_control = AlphaControlWidget()
        layout.addWidget(self.alpha_control)

        # controls
        control_layout = QHBoxLayout()
        self.repeat_spin = QSpinBox()
        self.repeat_spin.setRange(MIN_REPEATS, MAX_REPEATS)
        self.repeat_spin.setValue(DEFAULT_REPEATS)
        self.repeat_spin.setMaximumWidth(SPIN_WIDTH)
        
        self.run_button = make_button("Run Experiment", callback=self.on_run_callback, height=32)

        control_layout.addWidget(QLabel("Repeats:"))
        control_layout.addWidget(self.repeat_spin)
        control_layout.addWidget(self.run_button)
        control_layout.addStretch()
        layout.addLayout(control_layout)

    def set_placeholder(self, placeholder: str) -> None:
        """Set placeholder for parameter input field."""
        self.param_input.setPlaceholderText(placeholder)

    def get_alpha(self) -> float:
        """Return selected alpha level."""
        return self.alpha_control.value()

    def get_repeats(self) -> int:
        """Return entered repeats count."""
        return self.repeat_spin.value()

    def parse_params(self, messanger) -> tuple | None:
        """Parse parameters from string to float tuple."""
        params_str = self.param_input.text().strip()
        if not params_str:
            messanger.show_error("Invalid Parameters", "Please enter distribution parameters.")
            return None
        try:
            return tuple(map(float, params_str.split(',')))
        except ValueError:
            messanger.show_error("Invalid Parameters", "Parameters must be comma-separated numbers.")
            return None