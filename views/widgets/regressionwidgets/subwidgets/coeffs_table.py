from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTableWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from views.widgets.utils import (
    create_styled_result_table
)

RES_TABLE_HEIGHT = 160
BETA_TABLE_HEIGHT = 130


class RegrCoeffsTableWidget(QWidget):
    """Subwidget container for regression coefficients and beta coefficients tables."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize coefficient tables layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # coeffs table
        self.coeff_box = QGroupBox("Coefficients / Confidence Intervals")
        box_layout = QVBoxLayout(self.coeff_box)
        box_layout.setContentsMargins(4, 4, 4, 4)

        self.result_table = create_styled_result_table()
        self.result_table.setColumnCount(8)
        self.result_table.setHorizontalHeaderLabels([
            "Var", "CI Upper", "Coeff", "CI Lower", "Std.Error", "t-stat", "p-val", "significant"
        ])
        box_layout.addWidget(self.result_table)
        self.coeff_box.setFixedHeight(RES_TABLE_HEIGHT)
        layout.addWidget(self.coeff_box)

        # beta table
        self.beta_box = QGroupBox("Standardized (Beta) Coefficients")
        beta_layout = QVBoxLayout(self.beta_box)
        beta_layout.setContentsMargins(4, 4, 4, 4)

        self.beta_table = create_styled_result_table()
        self.beta_table.setColumnCount(2)
        self.beta_table.setHorizontalHeaderLabels(["Variable", "Beta coef"])
        beta_layout.addWidget(self.beta_table)
        self.beta_box.setFixedHeight(BETA_TABLE_HEIGHT)
        self.beta_box.setVisible(False)
        layout.addWidget(self.beta_box)

    def populate_coefficients(self, ci_result: dict) -> None:
        """Populate regression coefficients, confidence intervals and t-stats."""
        ci_df = ci_result['CI']
        t_stats = ci_result['t_stats']
        p_vals = ci_result['p_values']
        significant = ci_result['significant']

        n_rows = len(ci_df)
        self.result_table.clearContents()
        self.result_table.setRowCount(n_rows)

        bold_font = QFont()
        bold_font.setBold(True)

        for row_idx in range(n_rows):
            var_item = QTableWidgetItem(str(ci_df.loc[row_idx, "variable"]))
            var_item.setFont(bold_font)
            self.result_table.setItem(row_idx, 0, var_item)

            items = [
                f"{float(ci_df.loc[row_idx, 'ci_upper']):.4f}",
                f"{float(ci_df.loc[row_idx, 'coef']):.4f}",
                f"{float(ci_df.loc[row_idx, 'ci_lower']):.4f}",
                f"{float(ci_df.loc[row_idx, 'std_err']):.4f}",
                f"{float(t_stats[row_idx]):.4f}",
                f"{float(p_vals[row_idx]):.4f}",
                str(significant[row_idx])
            ]
            for col_idx, text in enumerate(items, start=1):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                self.result_table.setItem(row_idx, col_idx, item)

        self.result_table.resizeColumnsToContents()

    def populate_beta(self, std_result: dict | None) -> None:
        """Populate standardized beta coefficients table if available."""
        if std_result is None:
            self.beta_box.setVisible(False)
            return

        features = std_result['features']
        betas = std_result['beta_coef']

        self.beta_table.clearContents()
        self.beta_table.setRowCount(len(features))
        
        bold_font = QFont()
        bold_font.setBold(True)

        for i, (feat, beta) in enumerate(zip(features, betas)):
            feat_item = QTableWidgetItem(str(feat))
            feat_item.setFont(bold_font)
            self.beta_table.setItem(i, 0, feat_item)

            val_item = QTableWidgetItem(f"{float(beta):.4f}")
            val_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            self.beta_table.setItem(i, 1, val_item)

        self.beta_table.resizeColumnsToContents()
        self.beta_box.setVisible(True)

    def clear(self) -> None:
        """Clear coefficients and beta tables."""
        self.result_table.clearContents()
        self.result_table.setRowCount(0)
        self.beta_table.clearContents()
        self.beta_table.setRowCount(0)
        self.beta_box.setVisible(False)