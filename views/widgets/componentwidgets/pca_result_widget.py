from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QTableWidget, QGroupBox, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from services.ui_services import UIMessager
from controllers import ComponentController
from utils import AppContext
from utils.ui_styles import groupMargin, groupStyle
from utils.helpers import create_section_header


RES_TABLE_GROUP_HEIGHT = 160
EQUATION_GROUP_HEIGHT = 80
BETA_TABLE_GROUP_HEIGHT = 130



class PCAResultWidget(QWidget):
    """Widget for model post-fit summary (R^2, std.err., CI, etc.)."""
    def __init__(self, context: AppContext, component_controller: ComponentController):
        super().__init__()
        self.context: AppContext = context
        self.messanger: UIMessager = context.messanger
        self.controller: ComponentController = component_controller
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize PCA result UI components."""
        main_layout = QVBoxLayout(self)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        container = QWidget()
        container.setStyleSheet(groupStyle + groupMargin)
        container.setMaximumWidth(350)
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        header_layout = QHBoxLayout()
        layout.addLayout(create_section_header("PCA Results"))
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Build sections
        layout.addWidget(self._build_ev_group())
        layout.addWidget(self._init_result_table)
        layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _build_ev_group(self) -> QGroupBox:
        box = QGroupBox("Explained Variance")
        layout = QVBoxLayout()
        self.ev_label = QLabel("—")
        self.ev_label.setWordWrap(True)
        self.ev_label.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.ev_label)
        box.setLayout(layout)
        return box
    
    def _init_result_table(self, layout: QVBoxLayout) -> None:
        """Initialize PCA result table with original/transformed variables."""
        group = QGroupBox("PCA Result Table")
        ...

    def create_results(self) -> None:
        """Create and display PCA result."""
        try:
            ...
        except Exception as e:
            self.messanger.show_error("PCA result error", str(e))

    def _update_ev_group(self) -> None:
        """Update ev_group labels."""
        try:
            total_ev, evr = self.controller.get_explained_variance()
            lines = [f"Total explained variance: <b>{total_ev:.4f}</b>", ""]
            for i, v in enumerate(evr, start=1):
                lines.append(f"PC_{i}: {v:.4f} ({v*100:.1f}%)")
            self.ev_label.setText("<br>".join(lines))
        except Exception:
            self.ev_label.setText("—")

    def _update_result_table(self) -> None:
        """Update result table with original/transformed variables."""
        ...

    def refresh(self) -> None:
        """Refresh the state of the widget"""
        self._update_ev_group()
        self._update_result_table()

    def clear(self) -> None:
        """Clear all result data."""
        ...