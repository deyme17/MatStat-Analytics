from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QComboBox, QWidget

class RegrDependentVarSelectorWidget(QGroupBox):
    """Group widget for selecting target (dependent) variable Y."""
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Dependent Variable (Y)", parent)
        layout = QVBoxLayout(self)

        self.dependent_combo = QComboBox()
        layout.addWidget(QLabel("Target variable:"))
        layout.addWidget(self.dependent_combo)

    def populate(self, columns: list[str]) -> None:
        """Populate combobox options and select last item."""
        self.dependent_combo.clear()
        for col in columns:
            self.dependent_combo.addItem(col)
        if self.dependent_combo.count() > 0:
            self.dependent_combo.setCurrentIndex(self.dependent_combo.count() - 1)

    def get_selected_variable(self) -> str:
        """Return chosen target variable name."""
        return self.dependent_combo.currentText()