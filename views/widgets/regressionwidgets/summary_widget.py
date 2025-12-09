from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QGroupBox, QTableWidgetItem
)
from services.ui_services.messager import UIMessager
from utils import AppContext
from controllers import RegressionController
from utils.ui_styles import groupMargin, groupStyle

HEADING_TITLE_SIZE = 15
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

        self._init_result_table(layout)
        self._init_equation_label(layout)
        self._init_model_sagn_label(layout)
        self._init_metrics_section(layout)

        self.setLayout(layout)

    def _init_result_table(self, layout: QVBoxLayout) -> None:
        """Initialize regression result table with coefficients and CI."""
        group = QGroupBox("Coefficients / Confidence Intervals")
        group_layout = QVBoxLayout()
        
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(8)
        self.result_table.setHorizontalHeaderLabels([
            "Var", "CI Upper", "Coeff", "CI Lower", "Std.Error", "t-stat", "p-val", "sagnificant"
        ])
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.setAlternatingRowColors(True)

        group_layout.addWidget(self.result_table)
        group.setLayout(group_layout)
        group.setFixedHeight(RES_TABLE_GROUP_HEIGHT)
        layout.addWidget(group)

    def _init_equation_label(self, layout: QVBoxLayout) -> None:
        """Initialize model equation label (e.g. y = ax + b)."""
        group = QGroupBox("Model equation")
        group_layout = QVBoxLayout()
        self.model_equation_label = QLabel("-")
        group_layout.addWidget(self.model_equation_label)
        group.setLayout(group_layout)
        layout.addWidget(group)

    def _init_model_sagn_label(self, layout: QVBoxLayout) -> None:
        """Initialize model significance (F-test) section."""
        group = QGroupBox("Model Significance")
        group_layout = QVBoxLayout()
        self.model_sagn_label = QLabel("-")
        group_layout.addWidget(self.model_sagn_label)
        group.setLayout(group_layout)
        layout.addWidget(group)

    def _init_metrics_section(self, layout: QVBoxLayout) -> None:
        """Initialize metrics section."""
        group = QGroupBox("Model Metrics")
        group_layout = QVBoxLayout()
        self.metrics = QLabel("-")
        group_layout.addWidget(self.metrics)
        group.setLayout(group_layout)
        layout.addWidget(group)

    def create_summary(self, alpha: float = 0.05) -> None:
        """Create and display regression model summary."""
        try:
            summary = self.controller.summary()
            if not summary:
                self.messanger.show_info("No summary", "Model has not been fitted yet")
                return
            
            self._update_metrics(summary)
            self._update_equation_label(summary.get('equation', None))

            ci_result = self.controller.confidence_intervals(alpha=alpha)
            model_sagn = self.controller.model_sagnificance(alpha=alpha)
            if ci_result:
                self._update_coefficients_table(ci_result)
                self._update_model_sagn_label(model_sagn)
            
        except Exception as e:
            self.messanger.show_error("Summary error", str(e))

    def _update_metrics(self, summary: dict) -> None:
        """Update metrics labels."""
        metrics = summary.get('metrics', {})
        metric_lines = [f"{k} = {float(v):.4f}" for k, v in metrics.items()]
        metrics_str = "\n".join(metric_lines) + "\n"
        self.metrics.setText(metrics_str)

    def _update_coefficients_table(self, ci_result: dict) -> None:
        """Update coefficients table with CI and t-values."""
        ci_df = ci_result['CI']
        t_stats = ci_result['t_stats']
        p_vals = ci_result['p_values']
        sagnificant = ci_result['sagnificant']
        
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
            self.result_table.setItem(row_idx, 7, QTableWidgetItem(f"{str(sagnificant[row_idx])}"))

        self.result_table.resizeColumnsToContents()

    def _update_equation_label(self, equation: str | None) -> None:
        """Update model equation label."""
        if not equation:
            self.model_equation_label.setText("-")
            return
        self.model_equation_label.setText(equation)
        
    def _update_model_sagn_label(self, model_sagn: dict | None) -> None:
        """Update model F-test significance label."""
        if not model_sagn:
            self.model_sagn_label.setText("No F-test results available")
            return

        stat = model_sagn.get("stat", {})
        p_val = model_sagn.get("p_value", None)
        sagnificant = model_sagn.get("sagnificant", None)

        if stat is None or p_val is None:
            self.model_sagn_label.setText("Insufficient data for testing")
            return
        
        f_text = f"{stat.get('name', 'statistic')}: {float(stat.get('val', 0)):.4f} | p-value: {float(p_val):.4f} | Significant: {str(sagnificant)}"
        self.model_sagn_label.setText(f_text)

    def clear(self) -> None:
        """Clear all summary data."""
        self.metrics.setText("-")
        self.result_table.setRowCount(0)