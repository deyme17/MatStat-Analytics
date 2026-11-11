from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QComboBox
from PyQt6.QtCore import Qt
from services.ui_services import UIMessager
from controllers import FactorController
from utils import AppContext
from utils.ui_styles import groupMargin, groupStyle
from views.widgets.utils import create_section_header
from views.widgets.factorwidgets.subwidgets.pfm_matrix_table import PFMMatrixTableWidget


class PFMResultWidget(QWidget):
    """Widget for PFM post-fit report."""
    def __init__(self, context: AppContext, factor_controller: FactorController):
        super().__init__()
        self.context: AppContext = context
        self.messanger: UIMessager = context.messanger
        self.controller: FactorController = factor_controller
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize interface layout for PFM results."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setStyleSheet(groupStyle + groupMargin)
        container.setMaximumWidth(350)
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addLayout(create_section_header("PFM Results"))

        # summary
        self.summary_box = QGroupBox("Summary")
        sum_layout = QVBoxLayout(self.summary_box)
        self.summary_label = QLabel("—")
        self.summary_label.setWordWrap(True)
        sum_layout.addWidget(self.summary_label)
        layout.addWidget(self.summary_box)

        # tables
        self.loadings_table = PFMMatrixTableWidget("Factor Loadings (A)")
        self.corr_table = PFMMatrixTableWidget("Correlation Matrix (R)")
        layout.addWidget(self.loadings_table)
        layout.addWidget(self.corr_table)

        # iterations
        self.iter_box = QGroupBox("Iterations")
        iter_layout = QVBoxLayout(self.iter_box)
        self.iter_combo = QComboBox()
        self.iter_combo.currentIndexChanged.connect(self._on_iteration_changed)
        self.iter_label = QLabel("—")
        self.iter_loadings_table = PFMMatrixTableWidget("Loadings (A)")
        self.iter_rh_table = PFMMatrixTableWidget("Reduced matrix (R_h)")

        iter_layout.addWidget(self.iter_combo)
        iter_layout.addWidget(self.iter_label)
        iter_layout.addWidget(self.iter_loadings_table)
        iter_layout.addWidget(self.iter_rh_table)
        layout.addWidget(self.iter_box)

        layout.addStretch()
        main_layout.addWidget(container)

    def create_results(self) -> None:
        """Create and display PFM result after fit."""
        try:
            self._update_summary()
            self._update_loadings()
            self.corr_table.populate(self.controller.get_results()["R"])
            self._update_iterations()
        except Exception as e:
            self.messanger.show_error("PFM result error", str(e))

    def clear(self) -> None:
        """Clear all result data."""
        self.summary_label.setText("—")
        self.iter_label.setText("—")
        self.iter_combo.blockSignals(True)
        self.iter_combo.clear()
        self.iter_combo.blockSignals(False)
        for t in (self.loadings_table, self.corr_table, self.iter_loadings_table, self.iter_rh_table):
            t.clear()

    def _update_summary(self) -> None:
        """Updates summary group with fit results and statistics."""
        res = self.controller.get_results()
        stats = self.controller.get_statistics()
        status = res["result"].value if res["ok"] else f"<span style='color:#c62828'>{res['result'].value}</span>"
        lines = [
            f"Estimator: <b>{res['estimator']}</b>",
            f"Factors: <b>{res['n_factors']}</b>, iterations: <b>{res['n_iter']}</b>",
            f"Objective f: <b>{res['f']:.6f}</b>",
            f"Status: <b>{status}</b>",
            f"Total variance: <b>{stats['total_variance']:.3f}</b> ({stats['total_variance_share'] * 100:.1f}%)"
        ]
        self.summary_label.setText("<br>".join(lines))

    def _update_loadings(self) -> None:
        """Populate the final loadings table with communalities and factor contributions."""        
        res = self.controller.get_results()
        stats = self.controller.get_statistics()
        A = res["A"]
        df = A.copy()
        df["h²"] = res["h2"]
        df["d²"] = stats["uniqueness"]
        extra_rows = {
            "Contribution": [f"{v:.3f}" for v in stats["factor_var_contributions"]] + [f"{stats['total_variance']:.3f}", ""],
            "Share (%)": [f"{v:.1f}" for v in stats["factor_var_share"] * 100] + [f"{stats['total_variance_share'] * 100:.1f}", ""],
            "Cum. (%)": [f"{v:.1f}" for v in stats["cumulative_var_share"] * 100] + ["", ""],
        }
        self.loadings_table.populate(df, color_cols=A.shape[1], extra_rows=extra_rows)

    def _update_iterations_group(self) -> None:
        """Get fir history and update iteration group."""
        history = self.controller.get_history()
        self.iter_combo.blockSignals(True)
        self.iter_combo.clear()
        self.iter_combo.addItems([f"Iteration {h['iter']}" for h in history])
        self.iter_combo.setCurrentIndex(len(history) - 1)
        self.iter_combo.blockSignals(False)
        self._on_iteration_changed()

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
            self.iter_loadings_table.populate(df, color_cols=A.shape[1])
            self.iter_rh_table.populate(it["R_h"], highlight_diag=True)
        except Exception as e:
            self.messanger.show_error("Iteration error", str(e))