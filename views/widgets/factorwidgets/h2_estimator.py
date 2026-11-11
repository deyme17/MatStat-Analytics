from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QGroupBox
)


class H2EstimatorWidget(QGroupBox):
    """Widget for selecting communality estimator methods."""
    def __init__(self, estimators: list[str], parent: QWidget | None = None) -> None:
        super().__init__("Communality Estimator Selection", parent)
        layout = QVBoxLayout(self)

        self.combo = QComboBox()
        for method in estimators:
            self.combo.addItem(method)

        layout.addWidget(QLabel("h^2 Estimators:"))
        layout.addWidget(self.combo)

    def get_selected_estimator(self) -> str:
        """Return active estimator method name."""
        return self.combo.currentText()