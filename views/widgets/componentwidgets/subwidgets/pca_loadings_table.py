import pandas as pd
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QTableWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from views.widgets.utils import (
    create_styled_result_table, get_loading_heatmap_color, fit_table_height
)

MAX_RESULT_TABLE_HEIGHT = 400
SUMMARY_ROW_COLOR = "#e8eaf6"


class PCALoadingsTableWidget(QGroupBox):
    """Widget wrapper for PCA component matrix / loadings table."""
    def __init__(self, parent=None):
        super().__init__("Component Matrix", parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        
        self.table = create_styled_result_table()
        layout.addWidget(self.table)

    def populate(self, components, evr, eigenvalues, feature_names: list[str]) -> None:
        """Populate component loadings and summary statistics rows."""
        n_features, n_components = components.shape
        pc_labels = [f"PC_{i+1}" for i in range(n_components)]
        extra_rows = ["Eigenvalues", "EVR (%)", "Cum. EVR (%)"]

        self.table.clearContents()
        self.table.setRowCount(n_features + len(extra_rows))
        self.table.setColumnCount(n_components + 1)
        self.table.setHorizontalHeaderLabels([""] + pc_labels)

        bold_font = QFont()
        bold_font.setBold(True)

        # features
        for row_idx, feat in enumerate(feature_names):
            label_item = QTableWidgetItem(feat)
            label_item.setFont(bold_font)
            self.table.setItem(row_idx, 0, label_item)

            for col_idx in range(n_components):
                val = components[row_idx, col_idx]
                item = QTableWidgetItem(f"{val:.2f}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                item.setBackground(get_loading_heatmap_color(val))
                self.table.setItem(row_idx, col_idx + 1, item)

        # summary
        evr_pct = [v * 100 for v in evr]
        cumulative, acc = [], 0.0
        for v in evr_pct:
            acc += v
            cumulative.append(acc)

        summary_data = [eigenvalues[:n_components], evr_pct, cumulative]
        summary_fmt = ["{:.3f}", "{:.1f}", "{:.1f}"]

        for s_idx, (label, data, fmt) in enumerate(zip(extra_rows, summary_data, summary_fmt)):
            row_idx = n_features + s_idx
            label_item = QTableWidgetItem(label)
            label_item.setFont(bold_font)
            label_item.setBackground(QColor(SUMMARY_ROW_COLOR))
            self.table.setItem(row_idx, 0, label_item)

            for col_idx, val in enumerate(data):
                item = QTableWidgetItem(fmt.format(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                item.setBackground(QColor(SUMMARY_ROW_COLOR))
                self.table.setItem(row_idx, col_idx + 1, item)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        fit_table_height(self.table, max_h=MAX_RESULT_TABLE_HEIGHT)

    def clear(self) -> None:
        """Clear table contents."""
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        fit_table_height(self.table, max_h=MAX_RESULT_TABLE_HEIGHT)