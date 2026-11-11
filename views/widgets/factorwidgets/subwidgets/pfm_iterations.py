import pandas as pd
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QTableWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from views.widgets.utils import (
    create_styled_result_table, get_loading_heatmap_color, fit_table_height
)

MAX_RESULT_TABLE_HEIGHT = 400
SUMMARY_ROW_COLOR = "#e8eaf6"


class PFMMatrixTableWidget(QGroupBox):
    """Reusable table container for Factor Loadings (A), Correlation (R), or Reduced (R_h) matrices."""
    def __init__(self, title: str, parent=None):
        super().__init__(title, parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        self.table = create_styled_result_table()
        layout.addWidget(self.table)

    def populate(self, df: pd.DataFrame, fmt: str = "{:.3f}", color_cols: int = 0, 
                 highlight_diag: bool = False, extra_rows: dict[str, list[str]] | None = None) -> None:
        """Populate table values from a pandas DataFrame."""
        extra_rows = extra_rows or {}
        n_rows, n_cols = df.shape

        self.table.clearContents()
        self.table.setRowCount(n_rows + len(extra_rows))
        self.table.setColumnCount(n_cols + 1)
        self.table.setHorizontalHeaderLabels([""] + [str(c) for c in df.columns])

        bold_font = QFont()
        bold_font.setBold(True)

        # data rows
        for row_idx, (label, row) in enumerate(df.iterrows()):
            label_item = QTableWidgetItem(str(label))
            label_item.setFont(bold_font)
            self.table.setItem(row_idx, 0, label_item)

            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(fmt.format(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                if col_idx < color_cols:
                    item.setBackground(get_loading_heatmap_color(value))
                elif highlight_diag and col_idx == row_idx:
                    item.setBackground(QColor(SUMMARY_ROW_COLOR))
                self.table.setItem(row_idx, col_idx + 1, item)

        # extra summary rows
        for s_idx, (label, values) in enumerate(extra_rows.items()):
            row_idx = n_rows + s_idx
            label_item = QTableWidgetItem(label)
            label_item.setFont(bold_font)
            label_item.setBackground(QColor(SUMMARY_ROW_COLOR))
            self.table.setItem(row_idx, 0, label_item)

            for col_idx, text in enumerate(values):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                item.setBackground(QColor(SUMMARY_ROW_COLOR))
                self.table.setItem(row_idx, col_idx + 1, item)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        fit_table_height(self.table, max_h=MAX_RESULT_TABLE_HEIGHT)

    def clear(self) -> None:
        """Clear matrix table."""
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        fit_table_height(self.table, max_h=MAX_RESULT_TABLE_HEIGHT)