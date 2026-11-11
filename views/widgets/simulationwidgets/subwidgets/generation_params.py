from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QScrollArea, QFrame
)
from views.widgets.utils import create_section_header

CORR_AREA_SCROLL_SIZE = 500
CORR_LINE_EDIT_SIZE = 100
MIN_PARAM_INPUT_WIDTH = 200


class GenerationParamsWidget(QFrame):
    """Subwidget managing feature-specific parameters and correlation matrix input fields."""
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.correlation_inputs: list[tuple[QLabel, QLineEdit]] = []
        self.feature_param_inputs: list[QLineEdit] = []
        self._cached_placeholder: str = " "
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize parameters frame layout."""
        layout = QVBoxLayout(self)

        # feature params section
        layout.addWidget(QLabel("Feature-specific Parameters:"))
        self.feature_params_layout = QVBoxLayout()
        layout.addLayout(self.feature_params_layout)
        layout.addLayout(create_section_header(""))

        # corr matrix section
        layout.addWidget(QLabel("Correlation Coefficients:"))
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMaximumHeight(CORR_AREA_SCROLL_SIZE)

        self.correlation_container = QWidget()
        self.correlation_layout = QVBoxLayout(self.correlation_container)
        self.scroll_area.setWidget(self.correlation_container)

        layout.addWidget(self.scroll_area)

    def update_fields(self, n_features: int) -> None:
        """Rebuild parameter inputs and correlation fields based on n_features count."""
        self._clear_layout(self.correlation_layout)
        self._clear_layout(self.feature_params_layout)

        self.correlation_inputs.clear()
        self.feature_param_inputs.clear()

        # build feature params
        for i in range(n_features):
            _, line_edit, param_layout = self._create_input_row(
                label_text=f"feature {i+1} params:", 
                placeholder=self._cached_placeholder, 
                min_width=MIN_PARAM_INPUT_WIDTH
            )
            self.feature_params_layout.addLayout(param_layout)
            self.feature_param_inputs.append(line_edit)

        # build corr fields if n_features > 1
        corr_needed = n_features > 1
        self.scroll_area.setVisible(corr_needed)
        if corr_needed:
            for i in range(n_features):
                for j in range(i + 1, n_features):
                    label, line_edit, corr_layout = self._create_input_row(
                        label_text=f"corr{{col{i+1}, col{j+1}}}:", 
                        placeholder="0.0", 
                        max_width=CORR_LINE_EDIT_SIZE
                    )
                    self.correlation_layout.addLayout(corr_layout)
                    self.correlation_inputs.append((label, line_edit))

    def update_placeholder(self, placeholder: str) -> None:
        """Update placeholder text across all feature input fields."""
        self._cached_placeholder = placeholder
        for line_edit in self.feature_param_inputs:
            line_edit.setPlaceholderText(placeholder)

    def parse_params(self, messanger) -> list[tuple] | None:
        """Parse and validate feature-specific parameter tuples."""
        n_features = len(self.feature_param_inputs)
        params_list = []

        for i, line_edit in enumerate(self.feature_param_inputs):
            text = line_edit.text().strip()
            if not text:
                messanger.show_error("Invalid Parameters", f"Feature {i+1} parameters are required.")
                return None
            try:
                params = tuple(map(float, text.split(',')))
                params_list.append(params)
            except ValueError:
                messanger.show_error("Invalid Parameters", f"Feature {i+1} parameters must be comma-separated numbers.")
                return None

        if len(set(len(p) for p in params_list)) > 1 or len(params_list) < n_features:
            messanger.show_error("Invalid Parameters", "All features must have the same number of parameters (>= 1).")
            return None

        return params_list

    def parse_correlation_matrix(self, n_features: int, messanger) -> list[list[float]] | None:
        """Construct symmetric correlation matrix from inputs."""
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
                        val = float(text)
                        if not (-1 <= val <= 1):
                            messanger.show_error("Invalid Correlation", f"Correlation corr{{col{i+1}, col{j+1}}} must be between -1 and 1.")
                            return None
                        corr_matrix[i][j] = val
                        corr_matrix[j][i] = val
                except ValueError:
                    messanger.show_error("Invalid Correlation", f"Correlation corr{{col{i+1}, col{j+1}}} must be a valid number.")
                    return None

                input_idx += 1

        return corr_matrix

    def _create_input_row(self, label_text: str, placeholder: str, 
                          max_width: int | None = None, 
                          min_width: int | None = None) -> tuple[QLabel, QLineEdit, QHBoxLayout]:
        """Factory helper creating a labeled input row layout."""
        layout = QHBoxLayout()
        label = QLabel(label_text)
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)

        if max_width is not None:
            line_edit.setMaximumWidth(max_width)
        if min_width is not None:
            line_edit.setMinimumWidth(min_width)

        layout.addWidget(label)
        layout.addWidget(line_edit)
        layout.addStretch()
        return label, line_edit, layout

    def _clear_layout(self, layout: QVBoxLayout) -> None:
        """Helper to recursively clear layout content."""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())