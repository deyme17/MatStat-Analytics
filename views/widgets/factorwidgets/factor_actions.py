from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox
)
from views.widgets.utils import make_button


class FactorActionsWidget(QGroupBox):
    """Widget container for Factor analysis actions."""
    def __init__(self, on_fit: callable, on_clear: callable, parent: QWidget | None = None) -> None:
        super().__init__("Actions", parent)
        layout = QVBoxLayout(self)

        self.fit_btn = make_button("Fit Model", callback=on_fit, height=32)
        self.clear_btn = make_button("Clear", callback=on_clear, height=32)

        layout.addWidget(self.fit_btn)
        layout.addWidget(self.clear_btn)

    def set_fit_enabled(self, enabled: bool) -> None:
        """Set enablement status for fit button."""
        self.fit_btn.setEnabled(enabled)