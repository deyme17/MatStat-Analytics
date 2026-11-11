from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox
from PyQt6.QtCore import Qt
from services.ui_services import UIMessager
from controllers import ComponentController
from utils import AppContext
from utils.ui_styles import groupMargin, groupStyle
from views.widgets.utils import create_section_header
from .subwidgets import PCALoadingsTableWidget


class PCAResultWidget(QWidget):
    """Widget for PCA post-fit summary: explained variance and loadings table."""
    def __init__(self, context: AppContext, component_controller: ComponentController):
        super().__init__()
        self.context: AppContext = context
        self.messanger: UIMessager = context.messanger
        self.controller: ComponentController = component_controller
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize user interface for PCA results widget."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setStyleSheet(groupStyle + groupMargin)
        container.setMaximumWidth(350)
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addLayout(create_section_header("PCA Results"))

        # explained variance
        self.ev_box = QGroupBox("Explained Variance")
        ev_layout = QVBoxLayout(self.ev_box)
        self.ev_label = QLabel("—")
        self.ev_label.setWordWrap(True)
        ev_layout.addWidget(self.ev_label)
        layout.addWidget(self.ev_box)

        # loadings table widget
        self.loadings_widget = PCALoadingsTableWidget()
        layout.addWidget(self.loadings_widget)

        layout.addStretch()
        main_layout.addWidget(container)

    def create_results(self) -> None:
        """Create and display PCA result after fit/transform."""
        try:
            self._update_ev_group()
            components = self.controller.get_principal_components()
            if components is not None:
                _, evr = self.controller.get_explained_variance()
                eigenvalues = self.controller.get_eigenvalues()
                feature_names = list(self.controller.orig_X_df_.columns) if self.controller.orig_X_df_ is not None else [f"x{i+1}" for i in range(components.shape[0])]
                self.loadings_widget.populate(components, evr, eigenvalues, feature_names)
        except Exception as e:
            self.messanger.show_error("PCA result error", str(e))

    def refresh(self) -> None:
        """Refresh state after restoring original data."""
        self._update_ev_group()
        self.loadings_widget.clear()

    def clear(self) -> None:
        """Clear all result data."""
        self.ev_label.setText("—")
        self.loadings_widget.clear()

    def _update_ev_group(self) -> None:
        """Update explained variance label."""
        try:
            total_ev, evr = self.controller.get_explained_variance()
            lines = [f"Total explained variance: <b>{total_ev:.4f}</b>", ""]
            lines.extend([f"PC_{i}: {v:.4f} ({v * 100:.1f}%)" for i, v in enumerate(evr, start=1)])
            self.ev_label.setText("<br>".join(lines))
        except Exception:
            self.ev_label.setText("—")