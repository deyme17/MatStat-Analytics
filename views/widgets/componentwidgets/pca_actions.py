from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox
)
from views.widgets.utils import make_button


class PCAActionsWidget(QGroupBox):
    """Widget container for PCA transformation and restoration action buttons."""
    def __init__(self, callbacks: dict, parent: QWidget | None = None) -> None:
        super().__init__("Actions", parent)
        layout = QVBoxLayout(self)

        self.fit_btn = make_button("Fit Model", callback=callbacks.get("fit"), height=32)
        self.transform_btn = make_button("Transform Data", callback=callbacks.get("transform"), height=32)
        self.scree_btn = make_button("Show Scree Plot", callback=callbacks.get("scree"), height=32)
        self.inverse_btn = make_button("Inverse Transform (Reconstruct)", callback=callbacks.get("inverse"), height=32)
        self.original_btn = make_button("Restore Original Data", callback=callbacks.get("original"), height=32)

        for btn in (self.fit_btn, self.transform_btn, self.scree_btn, self.inverse_btn, self.original_btn):
            layout.addWidget(btn)

    def update_states(self, has_enough_features: bool, state: str, fitted_here: bool, is_inverse: bool) -> None:
        """Refresh button enablement states based on PCA state."""
        self.fit_btn.setEnabled(has_enough_features and (state != "transformed" or not fitted_here))
        self.transform_btn.setEnabled(has_enough_features and (state != "transformed" or not fitted_here))
        self.scree_btn.setEnabled(state in ("fitted", "transformed") and fitted_here)
        self.original_btn.setEnabled(state == "transformed" and fitted_here)
        self.inverse_btn.setEnabled(state == "transformed" and fitted_here and not is_inverse)