from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea,
    QTableWidget, QGroupBox, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from services.ui_services import UIMessager
from controllers import ComponentController
from utils import AppContext
from utils.ui_styles import groupMargin, groupStyle
from utils.helpers import create_section_header


RES_TABLE_GROUP_HEIGHT = 160
EQUATION_GROUP_HEIGHT = 80
BETA_TABLE_GROUP_HEIGHT = 130



class PCAResultWidget(QWidget):
    """Widget for PCA post-fit summary: explained variance and loadings table."""
    def __init__(self, context: AppContext, component_controller: ComponentController):
        super().__init__()
        self.context: AppContext = context
        self.messanger: UIMessager = context.messanger
        self.controller: ComponentController = component_controller
        self._init_ui()

    def _init_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        container.setStyleSheet(groupStyle + groupMargin)
        container.setMaximumWidth(350)
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addLayout(create_section_header("PCA Results"))

        layout.addWidget(self._build_ev_group())
        layout.addWidget(self._build_loadings_group())
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

    def _build_loadings_group(self) -> QGroupBox:
        """Build the PCA loadings / component matrix group box."""
        box = QGroupBox("Component Matrix")
        layout = QVBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)

        self.loadings_table = QTableWidget()
        self.loadings_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.loadings_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.loadings_table.setAlternatingRowColors(True)
        self.loadings_table.verticalHeader().setVisible(False)
        self.loadings_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.loadings_table.setStyleSheet("""
            QTableWidget {font-size: 11px;}
            QHeaderView::section {
                background-color: #e3f2fd;
                color: #131212;
                font-weight: bold;
                padding: 3px;
                border: 1px solid #bbdefb;
            }
            QTableWidget::item {padding: 2px 6px;}
        """)
        layout.addWidget(self.loadings_table)
        box.setLayout(layout)
        return box

    def create_results(self) -> None:
        """Create and display PCA result after fit/transform."""
        try:
            self._update_ev_group()
            self._update_loadings_table()
        except Exception as e:
            self.messanger.show_error("PCA result error", str(e))

    def refresh(self) -> None:
        """Refresh the state of the widget (called after restore-original)."""
        self._update_ev_group()
        self._clear_loadings_table()

    def clear(self) -> None:
        """Clear all result data."""
        self.ev_label.setText("—")
        self._clear_loadings_table()

    def _update_ev_group(self) -> None:
        try:
            total_ev, evr = self.controller.get_explained_variance()
            lines = [f"Total explained variance: <b>{total_ev:.4f}</b>", ""]
            for i, v in enumerate(evr, start=1):
                lines.append(f"PC_{i}: {v:.4f} ({v * 100:.1f}%)")
            self.ev_label.setText("<br>".join(lines))
        except Exception:
            self.ev_label.setText("—")

    def _update_loadings_table(self) -> None:
        """Populate the Component Matrix table."""
        try:
            components = self.controller.get_principal_components()
            if components is None:
                self._clear_loadings_table()
                return
            
            n_features, n_components = components.shape
            _, evr = self.controller.get_explained_variance()
            eigenvalues = self.controller.get_eigenvalues()[:n_components]

            # feature names
            if self.controller.orig_X_df_ is not None:
                feature_names = list(self.controller.orig_X_df_.columns)
            else:
                feature_names = [f"x{i+1}" for i in range(n_features)]

            pc_labels = [f"PC_{i+1}" for i in range(n_components)]

            # summary rows
            EXTRA_ROWS = ["Eigenvalues", "EVR (%)", "Cum. EVR (%)"]

            total_rows = n_features + len(EXTRA_ROWS)
            self.loadings_table.clearContents()
            self.loadings_table.setRowCount(total_rows)
            self.loadings_table.setColumnCount(n_components + 1)

            headers = [""] + pc_labels
            self.loadings_table.setHorizontalHeaderLabels(headers)

            bold_font = QFont()
            bold_font.setBold(True)

            # feature / loading rows
            for row_idx, feat in enumerate(feature_names):
                # row label
                label_item = QTableWidgetItem(feat)
                label_item.setFont(bold_font)
                self.loadings_table.setItem(row_idx, 0, label_item)

                for col_idx in range(n_components):
                    value = components[row_idx, col_idx]
                    item = QTableWidgetItem(f"{value:.2f}")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignVCenter)
                    abs_v = abs(value)
                    if abs_v >= 0.5:
                        item.setBackground(QColor("#f3bab6"))
                    elif abs_v <= 0.1:
                        item.setBackground(QColor("#d7ffde"))
                    else:
                        item.setBackground(QColor("#9ddff3"))
                    self.loadings_table.setItem(row_idx, col_idx + 1, item)

            # summary rows
            evr_pct = [v * 100 for v in evr]
            cumulative = []
            acc = 0.0
            for v in evr_pct:
                acc += v
                cumulative.append(acc)

            summary_data = [eigenvalues, evr_pct, cumulative]
            summary_fmt = ["{:.3f}", "{:.1f}", "{:.1f}"]

            for s_idx, (label, data, fmt) in enumerate(zip(EXTRA_ROWS, summary_data, summary_fmt)):
                row_idx = n_features + s_idx
                label_item = QTableWidgetItem(label)
                label_item.setFont(bold_font)
                label_item.setBackground(QColor("#e8eaf6"))
                self.loadings_table.setItem(row_idx, 0, label_item)

                for col_idx, val in enumerate(data):
                    item = QTableWidgetItem(fmt.format(val))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignVCenter)
                    item.setBackground(QColor("#e8eaf6"))
                    self.loadings_table.setItem(row_idx, col_idx + 1, item)

            self.loadings_table.resizeColumnsToContents()
            self.loadings_table.resizeRowsToContents()

            row_h = sum(self.loadings_table.rowHeight(r)
                        for r in range(self.loadings_table.rowCount()))
            
            header_h = self.loadings_table.horizontalHeader().height()
            self.loadings_table.setFixedHeight(min(row_h + header_h + 6, 400))
        except Exception as e:
            self.messanger.show_error("Loadings table error", str(e))

    def _clear_loadings_table(self) -> None:
        self.loadings_table.clearContents()
        self.loadings_table.setRowCount(0)
        self.loadings_table.setColumnCount(0)