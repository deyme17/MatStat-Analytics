from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QScrollArea

EQUATION_GROUP_HEIGHT = 80


class RegrInfoPanelsWidget(QWidget):
    """Subwidget grouping model equation, significance, metrics, and tolerance info boxes."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize information panels layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # equation
        eq_group = QGroupBox("Model equation")
        eq_layout = QVBoxLayout(eq_group)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.equation_label = QLabel("-")
        scroll.setWidget(self.equation_label)
        eq_layout.addWidget(scroll)
        eq_group.setFixedHeight(EQUATION_GROUP_HEIGHT)
        layout.addWidget(eq_group)

        # significance
        sig_group = QGroupBox("Model Significance")
        sig_layout = QVBoxLayout(sig_group)
        self.significance_label = QLabel("-")
        sig_layout.addWidget(self.significance_label)
        layout.addWidget(sig_group)

        # metrics
        met_group = QGroupBox("Model Metrics")
        met_layout = QVBoxLayout(met_group)
        self.metrics_label = QLabel("-")
        met_layout.addWidget(self.metrics_label)
        layout.addWidget(met_group)

        # 4. Tolerance Box
        tol_group = QGroupBox("Tolerance bounds")
        tol_layout = QVBoxLayout(tol_group)
        self.tolerance_label = QLabel("-")
        tol_layout.addWidget(self.tolerance_label)
        layout.addWidget(tol_group)

    def update_info(self, summary: dict, model_sagn: dict | None, tolerance: dict | None) -> None:
        """Update text outputs for all info panels."""
        # equation
        self.equation_label.setText(summary.get('equation', None) or "-")

        # metrics
        metrics = summary.get('metrics', {})
        metric_lines = [f"{k} = {float(v):.4f}" for k, v in metrics.items()]
        self.metrics_label.setText("\n".join(metric_lines) + "\n")

        # significance
        if not model_sagn:
            self.significance_label.setText("No F-test results available")
        else:
            stat = model_sagn.get("stat", {})
            p_val = model_sagn.get("p_value", None)
            sig = model_sagn.get("significant", False)
            if stat is None or p_val is None:
                self.significance_label.setText("Insufficient data for testing")
            else:
                self.significance_label.setText(
                    f"{stat.get('name', 'statistic')}: {float(stat.get('val', 0)):.4f} | "
                    f"p-value: {float(p_val):.4f} | Significant: {str(sig)}"
                )

        # tolerance
        if tolerance:
            sigma_hat = tolerance.get("var", "-")
            lower, upper = tolerance.get("CI", ("-", "-"))
            self.tolerance_label.setText(f"{lower:.3f} <= {sigma_hat:.3f} <= {upper:.3f}")

    def clear(self) -> None:
        """Reset text across all panels."""
        self.equation_label.setText("-")
        self.significance_label.setText("-")
        self.metrics_label.setText("-")
        self.tolerance_label.setText("-")