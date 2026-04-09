from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QTableWidget, QGroupBox, QTableWidgetItem, QPushButton
)
from PyQt6.QtCore import Qt
from services.ui_services.messager import UIMessager
from services.ui_services.renderers.graph_renderers import (
    RegressionPlotDialog, ResidualsFittedPlot
)
from utils import AppContext
from controllers import RegressionController
from utils.ui_styles import groupMargin, groupStyle

HEADING_TITLE_SIZE = 16
RES_TABLE_GROUP_HEIGHT = 160
EQUATION_GROUP_HEIGHT = 80
BETA_TABLE_GROUP_HEIGHT = 130


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
        self._init_beta_table(layout)
        self._init_equation_label(layout)
        self._init_model_sagn_label(layout)
        self._init_metrics_section(layout)
        self._init_tolerance_bounds(layout)

        # visualize regression
        self.visualize_btn = QPushButton("Visualize")
        self.visualize_btn.setVisible(False)
        self.visualize_btn.clicked.connect(self._on_visualize)
        layout.addWidget(self.visualize_btn)

        # show diagnostics plot
        self.show_diagnos_diag_btn = QPushButton("Show Diagnostics")
        self.show_diagnos_diag_btn.setVisible(False)
        self.show_diagnos_diag_btn.clicked.connect(self._on_show_diagnostics)
        layout.addWidget(self.show_diagnos_diag_btn)

        self.setLayout(layout)

    def _init_result_table(self, layout: QVBoxLayout) -> None:
        """Initialize regression result table with coefficients and CI."""
        group = QGroupBox("Coefficients / Confidence Intervals")
        group_layout = QVBoxLayout()
        
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(8)
        self.result_table.setHorizontalHeaderLabels([
            "Var", "CI Upper", "Coeff", "CI Lower", "Std.Error", "t-stat", "p-val", "significant"
        ])
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.setAlternatingRowColors(True)

        group_layout.addWidget(self.result_table)
        group.setLayout(group_layout)
        group.setFixedHeight(RES_TABLE_GROUP_HEIGHT)
        layout.addWidget(group)

    def _init_beta_table(self, layout: QVBoxLayout) -> None:
        """Initialize standardized (beta) coefficients table."""
        self.beta_group = QGroupBox("Standardized (Beta) Coefficients")
        group_layout = QVBoxLayout()

        self.beta_table = QTableWidget()
        self.beta_table.setColumnCount(2)
        self.beta_table.setHorizontalHeaderLabels(["Variable", "Beta coef"])
        self.beta_table.horizontalHeader().setStretchLastSection(True)
        self.beta_table.setAlternatingRowColors(True)

        group_layout.addWidget(self.beta_table)
        self.beta_group.setLayout(group_layout)
        self.beta_group.setFixedHeight(BETA_TABLE_GROUP_HEIGHT)
        self.beta_group.setVisible(False)
        layout.addWidget(self.beta_group)

    def _init_equation_label(self, layout: QVBoxLayout) -> None:
        """Initialize model equation label (e.g. y = ax + b)."""
        group = QGroupBox("Model equation")
        group_layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.model_equation_label = QLabel("-")
        scroll_area.setWidget(self.model_equation_label)
        group_layout.addWidget(scroll_area)
        group.setLayout(group_layout)
        group.setFixedHeight(EQUATION_GROUP_HEIGHT)
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

    def _init_tolerance_bounds(self, layout: QVBoxLayout) -> None:
        """Initialize tolerance bounds section for residual variance"""
        group = QGroupBox("Tolerance bounds")
        group_layout = QVBoxLayout()
        self.tolerance = QLabel("-")
        group_layout.addWidget(self.tolerance)
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
            tol_result = self.controller.predict_tolerance(alpha=alpha)
            model_sagn = self.controller.model_significance(alpha=alpha)
            if ci_result:
                self._update_coefficients_table(ci_result)
                self._update_model_sagn_label(model_sagn)
            if tol_result:
                self.update_tolerance_label(tol_result)

            self._update_beta_table()

            n_features = len(self.controller.current_features)
            self.visualize_btn.setVisible(1 <= n_features <= 2)
            self.show_diagnos_diag_btn.setVisible(True)

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
        significant = ci_result['significant']
        
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
            self.result_table.setItem(row_idx, 7, QTableWidgetItem(f"{str(significant[row_idx])}"))

        self.result_table.resizeColumnsToContents()

    def _update_beta_table(self) -> None:
        """Update standardized beta coefficients table, or hide it if not supported."""
        std_result = self.controller.standardized_coefficients()
        if std_result is None:
            self.beta_group.setVisible(False)
            return

        features: list = std_result['features']
        betas = std_result['beta_coef']

        self.beta_table.setRowCount(len(features))
        for i, (feat, beta) in enumerate(zip(features, betas)):
            self.beta_table.setItem(i, 0, QTableWidgetItem(str(feat)))
            self.beta_table.setItem(i, 1, QTableWidgetItem(f"{float(beta):.4f}"))

        self.beta_table.resizeColumnsToContents()
        self.beta_group.setVisible(True)

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
        significant = model_sagn.get("significant", False)

        if stat is None or p_val is None:
            self.model_sagn_label.setText("Insufficient data for testing")
            return

        f_text = (
            f"{stat.get('name', 'statistic')}: {float(stat.get('val', 0)):.4f} | "
            f"p-value: {float(p_val):.4f} | "
            f"Significant: {str(significant)}"
        )
        self.model_sagn_label.setText(f_text)

    def update_tolerance_label(self, tolerance: dict | None) -> None:
        """Updates tolerance bounds label"""
        if tolerance is None:
            return
        sigma_hat = tolerance.get("var", "-")
        lower, upper = tolerance.get("CI", ("-", "-"))
        text = f"{lower:.3f} <= {sigma_hat:.3f} <= {upper:.3f}"
        self.tolerance.setText(text)

    def _on_visualize(self) -> None:
        """Open regression plot dialog."""
        try:
            data_model = self.context.data_model
            if data_model is None or data_model.dataframe is None:
                return

            features = self.controller.current_features
            target = self.controller.current_target
            df = data_model.dataframe

            missing = [c for c in features + [target] if c not in df.columns]
            if missing:
                self.messanger.show_error("Visualize error",
                    f"Columns not found in dataframe: {', '.join(missing)}")
                return

            X_df = df[features]
            y_series = df[target]

            dialog = RegressionPlotDialog(
                X_df=X_df,
                y_series=y_series,
                predict_fn=self.controller.predict,
                parent=self,
            )
            dialog.exec()

        except Exception as e:
            self.messanger.show_error("Visualize error", str(e))

    def _on_show_diagnostics(self) -> None:
        """Show regression diagnostics plots."""
        try:
            residuals = self.controller.current_residuals
            fitted = self.controller.current_fitted_values
            
            if residuals.size == 0 or fitted.size == 0:
                self.messanger.show_error("Warning", "No data for diagnostics. Fit the model first.")
                return

            dialog = ResidualsFittedPlot(
                residuals=residuals,
                fitted=fitted,
                parent=self
            )
            dialog.exec()
        except Exception as e:
            self.messanger.show_error("Diagnostics error", str(e))

    def clear(self) -> None:
        """Clear all summary data."""
        self.metrics.setText("-")
        self.tolerance.setText("-")
        self.result_table.setRowCount(0)
        self.beta_table.setRowCount(0)
        self.beta_group.setVisible(False)
        self.visualize_btn.setVisible(False)
        self.show_diagnos_diag_btn.setVisible(False)