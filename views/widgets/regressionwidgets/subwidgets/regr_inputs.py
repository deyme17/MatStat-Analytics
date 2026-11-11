from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QWidget, QFormLayout, QLineEdit, QScrollArea

MAX_X_INPUT_SECTION_HEIGHT = 200


class RegrInputsWidget(QGroupBox):
    """Subwidget managing dynamic feature input fields for regression prediction."""
    def __init__(self, parent=None):
        super().__init__("Input Feature Values", parent)
        self.feature_inputs: dict[str, QLineEdit] = {}
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize form layout wrapped inside QScrollArea."""
        self.form_layout = QFormLayout()

        self.inputs_container = QWidget()
        self.inputs_container.setLayout(self.form_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.inputs_container)
        scroll.setMaximumHeight(MAX_X_INPUT_SECTION_HEIGHT)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

    def setup_features(self, feature_names: list[str]) -> None:
        """Clear previous rows and construct new feature input fields."""
        self.feature_inputs.clear()
        while self.form_layout.rowCount() > 0:
            self.form_layout.removeRow(0)

        for feature in feature_names:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Enter value for {feature}")
            self.feature_inputs[feature] = line_edit
            self.form_layout.addRow(f"{feature}:", line_edit)

    def parse_input_data(self, messanger) -> dict[str, float] | None:
        """Parse text inputs into a float dictionary."""
        if not self.feature_inputs:
            messanger.show_info("No model", "Please fit a model first")
            return None

        input_data = {}
        for feature, line_edit in self.feature_inputs.items():
            val_str = line_edit.text().strip()
            if not val_str:
                messanger.show_error("Input error", f"Please enter a value for {feature}")
                return None
            try:
                input_data[feature] = float(val_str)
            except ValueError:
                messanger.show_error("Input error", f"Invalid number for {feature}: {val_str}")
                return None

        return input_data

    def clear(self) -> None:
        """Clear all input text fields."""
        for line_edit in self.feature_inputs.values():
            line_edit.clear()