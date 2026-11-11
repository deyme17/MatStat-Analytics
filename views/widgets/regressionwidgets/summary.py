from PyQt6.QtWidgets import QWidget, QVBoxLayout
from services.ui_services.messager import UIMessager
from services.ui_services.renderers.graph_renderers import RegressionPlot, ResidualsFittedPlot
from controllers import RegressionController
from utils import AppContext
from utils.ui_styles import groupMargin, groupStyle
from views.widgets.utils import create_section_header, make_button
from views.widgets.regressionwidgets.subwidgets import RegrCoeffsTableWidget, RegrInfoPanelsWidget


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
        layout = QVBoxLayout(self)

        layout.addLayout(create_section_header("Summary"))

        self.tables_widget = RegrCoeffsTableWidget()
        layout.addWidget(self.tables_widget)

        self.info_panels = RegrInfoPanelsWidget()
        layout.addWidget(self.info_panels)

        self.visualize_btn = make_button("Visualize", callback=self._on_visualize, height=32)
        self.visualize_btn.setVisible(False)
        layout.addWidget(self.visualize_btn)

        self.show_diagnos_diag_btn = make_button("Show Diagnostics", callback=self._on_show_diagnostics, height=32)
        self.show_diagnos_diag_btn.setVisible(False)
        layout.addWidget(self.show_diagnos_diag_btn)

    def create_summary(self, alpha: float = 0.05) -> None:
        """Create and display regression model summary."""
        try:
            summary = self.controller.summary()
            if not summary:
                self.messanger.show_info("No summary", "Model has not been fitted yet")
                return

            ci_result = self.controller.confidence_intervals(alpha=alpha)
            tol_result = self.controller.predict_tolerance(alpha=alpha)
            model_sagn = self.controller.model_significance(alpha=alpha)

            if ci_result:
                self.tables_widget.populate_coefficients(ci_result)
            self.tables_widget.populate_beta(self.controller.standardized_coefficients())
            self.info_panels.update_info(summary, model_sagn, tol_result)

            n_features = len(self.controller.current_features)
            self.visualize_btn.setVisible(1 <= n_features <= 2)
            self.show_diagnos_diag_btn.setVisible(True)

        except Exception as e:
            self.messanger.show_error("Summary error", str(e))

    def _on_visualize(self) -> None:
        """Open regression plot dialog."""
        try:
            df = self.context.data_model.dataframe if self.context.data_model else None
            if df is None:
                return

            features, target = self.controller.current_features, self.controller.current_target
            missing = [c for c in features + [target] if c not in df.columns]
            if missing:
                self.messanger.show_error("Visualize error", f"Columns not found: {', '.join(missing)}")
                return

            dialog = RegressionPlot(
                X_df=df[features],
                y_series=df[target],
                predict_fn=self.controller.predict,
                interval_fn=lambda dataframe: self.controller.confidence_band(dataframe),
                parent=self,
            )
            dialog.exec()
        except Exception as e:
            self.messanger.show_error("Visualize error", str(e))

    def _on_show_diagnostics(self) -> None:
        """Show regression diagnostics plots."""
        try:
            residuals, fitted = self.controller.current_residuals, self.controller.current_fitted_values
            if residuals.size == 0 or fitted.size == 0:
                self.messanger.show_error("Warning", "No data for diagnostics. Fit the model first.")
                return

            dialog = ResidualsFittedPlot(residuals=residuals, fitted=fitted, parent=self)
            dialog.exec()
        except Exception as e:
            self.messanger.show_error("Diagnostics error", str(e))

    def clear(self) -> None:
        """Clear all summary data."""
        self.tables_widget.clear()
        self.info_panels.clear()
        self.visualize_btn.setVisible(False)
        self.show_diagnos_diag_btn.setVisible(False)