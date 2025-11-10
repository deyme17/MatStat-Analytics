from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox,
    QTableWidget, QGroupBox, QTableWidgetItem
)
from services.ui_services.messager import UIMessager
from utils import AppContext
from controllers import RegressionController
from utils.ui_styles import groupMargin, groupStyle

HEADING_TITLE_SIZE = 15
ALPHA_MIN, ALPHA_MAX = 0.01, 0.99
ALPHA_STEP = 0.01
ALPHA_PRECISION = 2
DEFAULT_ALPHA = 0.05
HEADING_TITLE_SIZE = 16
RES_TABLE_GROUP_HEIGHT = 160


class RegrSummaryWidget(QWidget):
    """Widget for model post-fit summary (R^2, std.err., CI, etc.)."""
    def __init__(self, context: AppContext, regr_controller: RegressionController):
        super().__init__()
        self.context: AppContext = context
        self.messanger: UIMessager = context.messanger
        self.controller: RegressionController = regr_controller
        self._init_ui()


    def _init_ui(self) -> None:
        """Initialize regression summary UI components."""
        self.setStyleSheet(groupStyle + groupMargin)
        layout = QVBoxLayout()
        
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel(f"{'=' * HEADING_TITLE_SIZE} Summary {'=' * HEADING_TITLE_SIZE}"))
        header_layout.addStretch()
        layout.addLayout(header_layout)

        self._init_alpha_controls(layout)
        self._init_result_table(layout)
        self._init_metrics_section(layout)

        self.setLayout(layout)

    def _init_alpha_controls(self, layout: QVBoxLayout) -> None:
        """Initialize significance level controls."""
        self.alpha_spinbox = QDoubleSpinBox()
        self.alpha_spinbox.setRange(ALPHA_MIN, ALPHA_MAX)
        self.alpha_spinbox.setSingleStep(ALPHA_STEP)
        self.alpha_spinbox.setDecimals(ALPHA_PRECISION)
        self.alpha_spinbox.setValue(DEFAULT_ALPHA)
        self.alpha_spinbox.valueChanged.connect(self.create_summary)

        alpha_layout = QHBoxLayout()
        alpha_layout.addWidget(QLabel("Significance level α:"))
        alpha_layout.addWidget(self.alpha_spinbox)
        alpha_layout.addStretch()

        layout.addLayout(alpha_layout)

    def _init_result_table(self, layout: QVBoxLayout) -> None:
        """Initialize regression result table with coefficients and CI."""
        group = QGroupBox("Coefficients / Confidence Intervals")
        group_layout = QVBoxLayout()
        
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(7)
        self.result_table.setHorizontalHeaderLabels([
            "Var", "CI Upper", "Coeff", "CI Lower", "Std.Error", "t-stat", "p-val"
        ])
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.setAlternatingRowColors(True)

        group_layout.addWidget(self.result_table)
        group.setLayout(group_layout)
        group.setFixedHeight(RES_TABLE_GROUP_HEIGHT)
        layout.addWidget(group)

    def _init_metrics_section(self, layout: QVBoxLayout) -> None:
        """Initialize metrics section."""
        group = QGroupBox("Model Metrics")
        group_layout = QVBoxLayout()
        self.r2_label = QLabel("R²: -")
        for label in [self.r2_label]:
            label.setStyleSheet("font-weight: bold;")
            group_layout.addWidget(label)
        
        group.setLayout(group_layout)
        layout.addWidget(group)

    def create_summary(self) -> None:
        """Create and display regression model summary."""
        try:
            summary = self.controller.summary()
            if not summary:
                self.messanger.show_info("No summary", "Model has not been fitted yet")
                return
            
            self._update_metrics(summary)

            alpha = self.alpha_spinbox.value()
            ci_result = self.controller.confidence_intervals(alpha=alpha)
            if ci_result:
                self._update_coefficients_table(ci_result)
            
        except Exception as e:
            self.messanger.show_error("Summary error", str(e))

    def _update_metrics(self, summary: dict) -> None:
        """Update metrics labels."""
        r2 = summary.get('r_squared', None)
        self.r2_label.setText(f"R²: {r2:.6f}" if r2 is not None else "R²: -")

    def _update_coefficients_table(self, ci_result: dict) -> None:
        """Update coefficients table with CI and t-values."""
        ci_df = ci_result['CI']
        t_stats = ci_result['t_stats']
        p_vals = ci_result['p_values']
        
        n_rows = len(ci_df)
        self.result_table.setRowCount(n_rows)

        for row_idx in range(n_rows):
            self.result_table.setItem(row_idx, 0, QTableWidgetItem(str(ci_df.loc[row_idx, "variable"])))
            self.result_table.setItem(row_idx, 1, QTableWidgetItem(f"{float(ci_df.loc[row_idx, 'ci_upper']):.4f}"))
            self.result_table.setItem(row_idx, 2, QTableWidgetItem(f"{float(ci_df.loc[row_idx, 'coef']):.4f}"))
            self.result_table.setItem(row_idx, 3, QTableWidgetItem(f"{float(ci_df.loc[row_idx, 'ci_lower']):.4f}"))
            self.result_table.setItem(row_idx, 4, QTableWidgetItem(f"{float(ci_df.loc[row_idx, 'std_err']):.4f}"))
            self.result_table.setItem(row_idx, 5, QTableWidgetItem(f"{float(t_stats[row_idx]):.4f}"))
            self.result_table.setItem(row_idx, 6, QTableWidgetItem(f"{float(p_vals[row_idx]):.4f}"))

        self.result_table.resizeColumnsToContents()

    def clear(self) -> None:
        """Clear all summary data."""
        self.r2_label.setText("R²: -")
        self.result_table.setRowCount(0)