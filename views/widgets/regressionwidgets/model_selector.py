from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QComboBox, QWidget


class RegrModelSelectorWidget(QGroupBox):
    """Group widget for selecting target regression algorithm."""
    def __init__(self, model_names: list[str], parent: QWidget | None = None) -> None:
        super().__init__("Model Selection", parent)
        layout = QVBoxLayout(self)

        self.model_combo = QComboBox()
        for name in model_names:
            self.model_combo.addItem(name)

        layout.addWidget(QLabel("Regression model:"))
        layout.addWidget(self.model_combo)

    def get_selected_model(self) -> str:
        """Return chosen regression model name."""
        return self.model_combo.currentText()