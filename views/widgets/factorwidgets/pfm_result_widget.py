import pandas as pd

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox,
    QTableWidget, QGroupBox, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from services.ui_services import UIMessager
from controllers import FactorController
from utils import AppContext
from utils.ui_styles import groupMargin, groupStyle
from views.widgets.utils import create_section_header


MAX_TABLE_HEIGHT = 400
SUMMARY_COLOR = "#e8eaf6"



class PFMResultWidget(QWidget):
    """
    Widget for PFM post-fit report: summary, factor loadings, correlation matrix
    and loadings / reduced matrix of every iteration.
    """
    def __init__(self, context: AppContext, factor_controller: FactorController):
        super().__init__()
        self.context: AppContext = context
        self.messanger: UIMessager = context.messanger
        self.controller: FactorController = factor_controller
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize unit inteface for PCA results widget."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setStyleSheet(groupStyle + groupMargin)
        container.setMaximumWidth(350)
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addLayout(create_section_header("PFM Results"))

        layout.addWidget(self._build_summary_group())
        layout.addWidget(self._build_loadings_group())
        layout.addWidget(self._build_corr_group())
        layout.addWidget(self._build_iterations_group())
        layout.addStretch()

        main_layout.addWidget(container)

    def _build_summary_group(self) -> QGroupBox:
        """Build summary group for PFM."""
        box = QGroupBox("Summary")
        layout = QVBoxLayout()
        self.summary_label = QLabel("—")
        self.summary_label.setWordWrap(True)
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.summary_label)
        box.setLayout(layout)
        return box

    def _build_loadings_group(self) -> QGroupBox:
        """Build the final factor loadings matrix group box."""
        box = QGroupBox("Factor Loadings (A)")
        layout = QVBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        self.loadings_table = self._build_table()
        layout.addWidget(self.loadings_table)
        box.setLayout(layout)
        return box

    def _build_corr_group(self) -> QGroupBox:
        """Build the final factor loadings matrix group box."""
        box = QGroupBox("Correlation Matrix (R)")
        layout = QVBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        self.corr_table = self._build_table()
        layout.addWidget(self.corr_table)
        box.setLayout(layout)
        return box

    def _build_iterations_group(self) -> QGroupBox:
        """Build the group with loadings and reduced matrix of every iteration."""
        box = QGroupBox("Iterations")
        layout = QVBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)

        self.iter_combo = QComboBox()
        self.iter_combo.currentIndexChanged.connect(self._on_iteration_changed)
        self.iter_label = QLabel("—")
        self.iter_loadings_table = self._build_table()
        self.iter_rh_table = self._build_table()

        layout.addWidget(self.iter_combo)
        layout.addWidget(self.iter_label)
        layout.addWidget(QLabel("Loadings (A):"))
        layout.addWidget(self.iter_loadings_table)
        layout.addWidget(QLabel("Reduced matrix (R_h):"))
        layout.addWidget(self.iter_rh_table)
        box.setLayout(layout)
        return box

    @staticmethod
    def _build_table() -> QTableWidget:
        """Helper for building a table."""
        table = QTableWidget()
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        table.setStyleSheet("""
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
        return table

    # --- api ---

    def create_results(self) -> None:
        """Create and display PFM result after fit."""
        try:
            self._update_summary_group()
            self._update_loadings_table()
            self._update_corr_table()
            self._update_iterations_group()
        except Exception as e:
            self.messanger.show_error("PFM result error", str(e))

    def clear(self) -> None:
        """Clear all result data."""
        self.summary_label.setText("—")
        self.iter_label.setText("—")
        self.iter_combo.blockSignals(True)
        self.iter_combo.clear()
        self.iter_combo.blockSignals(False)
        for table in (self.loadings_table, self.corr_table,
                      self.iter_loadings_table, self.iter_rh_table):
            self._clear_table(table)

    # --- updates ---

    def _update_summary_group(self) -> None:
        """Updates summary group with fit results and statistics."""
        res = self.controller.get_results()
        stats = self.controller.get_statistics()

        status = res["result"].value
        if not res["ok"]:
            status = f"<span style='color:#c62828'>{status}</span>"

        lines = [
            f"Estimator: <b>{res['estimator']}</b>",
            f"Factors: <b>{res['n_factors']}</b>, iterations: <b>{res['n_iter']}</b>",
            f"Objective f: <b>{res['f']:.6f}</b>",
            f"Status: <b>{status}</b>",
            f"Total variance: <b>{stats['total_variance']:.3f}</b> "
            f"({stats['total_variance_share'] * 100:.1f}%)",
        ]
        self.summary_label.setText("<br>".join(lines))

    def _update_loadings_table(self) -> None:
        """Populate the final loadings table with communalities and factor contributions."""
        res = self.controller.get_results()
        stats = self.controller.get_statistics()

        A = res["A"]
        df = A.copy()
        df["h²"] = res["h2"]
        df["d²"] = stats["uniqueness"]

        contrib = stats["factor_var_contributions"]
        share = stats["factor_var_share"] * 100
        cum = stats["cumulative_var_share"] * 100
        total = stats["total_variance"]
        total_share = stats["total_variance_share"] * 100
        extra_rows = {
            "Contribution": [f"{v:.3f}" for v in contrib] + [f"{total:.3f}", ""],
            "Share (%)": [f"{v:.1f}" for v in share] + [f"{total_share:.1f}", ""],
            "Cum. (%)": [f"{v:.1f}" for v in cum] + ["", ""],
        }
        self._fill_table(self.loadings_table, df, color_cols=A.shape[1], extra_rows=extra_rows)

    def _update_corr_table(self) -> None:
        """Get correlation matrix and update table."""
        R = self.controller.get_results()["R"]
        self._fill_table(self.corr_table, R)

    def _update_iterations_group(self) -> None:
        """Get fir history and update iteration group."""
        history = self.controller.get_history()
        self.iter_combo.blockSignals(True)
        self.iter_combo.clear()
        self.iter_combo.addItems([f"Iteration {h['iter']}" for h in history])
        self.iter_combo.setCurrentIndex(len(history) - 1)
        self.iter_combo.blockSignals(False)
        self._on_iteration_changed()

    # --- callbacks ---

    def _on_iteration_changed(self) -> None:
        """Callback on changing history iteration."""
        idx = self.iter_combo.currentIndex()
        if idx < 0:
            return
        try:
            it = self.controller.get_iteration(idx)
            A = it["A"]
            df = A.copy()
            df["h²"] = it["h2"].to_numpy()
            self.iter_label.setText(f"Objective f: <b>{it['f']:.6f}</b>")
            self._fill_table(self.iter_loadings_table, df, color_cols=A.shape[1])
            self._fill_table(self.iter_rh_table, it["R_h"], highlight_diag=True)
        except Exception as e:
            self.messanger.show_error("Iteration error", str(e))

    # --- helpers ---

    def _fill_table(self, table: QTableWidget, df: pd.DataFrame,
                    fmt: str = "{:.3f}",
                    color_cols: int = 0,
                    highlight_diag: bool = False,
                    extra_rows: dict[str, list[str]] | None = None) -> None:
        """
        Populate table from a DataFrame (index -> row labels, columns -> headers).
        Args:
            table: Table to populate.
            df: Labeled values.
            fmt: Format of the values.
            color_cols: Number of leading columns colored by |value| (loadings).
            highlight_diag: Highlight the diagonal (communalities in R_h).
            extra_rows: Summary rows {label: [formatted value per df column]}.
        """
        extra_rows = extra_rows or {}
        n_rows, n_cols = df.shape

        table.clearContents()
        table.setRowCount(n_rows + len(extra_rows))
        table.setColumnCount(n_cols + 1)
        table.setHorizontalHeaderLabels([""] + [str(c) for c in df.columns])

        bold_font = QFont()
        bold_font.setBold(True)

        # data rows
        for row_idx, (label, row) in enumerate(df.iterrows()):
            label_item = QTableWidgetItem(str(label))
            label_item.setFont(bold_font)
            table.setItem(row_idx, 0, label_item)

            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(fmt.format(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignVCenter)
                if col_idx < color_cols:
                    item.setBackground(self._loading_color(value))
                elif highlight_diag and col_idx == row_idx:
                    item.setBackground(QColor(SUMMARY_COLOR))
                table.setItem(row_idx, col_idx + 1, item)

        # summary rows
        for s_idx, (label, values) in enumerate(extra_rows.items()):
            row_idx = n_rows + s_idx
            label_item = QTableWidgetItem(label)
            label_item.setFont(bold_font)
            label_item.setBackground(QColor(SUMMARY_COLOR))
            table.setItem(row_idx, 0, label_item)

            for col_idx, text in enumerate(values):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignVCenter)
                item.setBackground(QColor(SUMMARY_COLOR))
                table.setItem(row_idx, col_idx + 1, item)

        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        self._fit_table_height(table)

    @staticmethod
    def _loading_color(value: float) -> QColor:
        abs_v = abs(value)
        if abs_v >= 0.5:
            return QColor("#f3bab6")
        if abs_v <= 0.1:
            return QColor("#d7ffde")
        return QColor("#9ddff3")

    @staticmethod
    def _fit_table_height(table: QTableWidget) -> None:
        row_h = sum(table.rowHeight(r) for r in range(table.rowCount()))
        header_h = table.horizontalHeader().height()
        scroll_h = table.horizontalScrollBar().sizeHint().height()
        table.setFixedHeight(min(row_h + header_h + scroll_h + 6, MAX_TABLE_HEIGHT))

    def _clear_table(self, table: QTableWidget) -> None:
        table.clearContents()
        table.setRowCount(0)
        table.setColumnCount(0)
        self._fit_table_height(table)