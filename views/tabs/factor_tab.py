from views.widgets.utils.base_analysis_tab import BaseAnalysisTab
from views.widgets.factorwidgets import (
    FactorParamsWidget, H2EstimatorWidget, FactorActionsWidget, PFMResultWidget
)
from controllers import FactorController
from views.widgets.utils import update_status_label
from utils import AppContext, Event

MIN_FEATURES = 3


class FactorTab(BaseAnalysisTab):
    """Factor analysis tab that implements Principal Factor Analysis."""
    def __init__(self, context: AppContext, factor_controller: FactorController):
        """
        Args:
            context: Shared application context (data_model, event_bus, messager).
            factor_controller: Controller for performing factor analysis.
        """
        self.controller: FactorController = factor_controller
        super().__init__(context, title="PFM Config")
        self._refresh_buttons()

    def _build_custom_ui(self) -> None:
        """Build parameters, estimator selector, and actions for PFM."""
        self.params_widget = FactorParamsWidget()
        self.layout.addWidget(self.params_widget)

        self.h2_widget = H2EstimatorWidget(self.controller.get_h2_estimators_names())
        self.layout.addWidget(self.h2_widget)

        self.actions_widget = FactorActionsWidget(on_fit=self._on_fit, on_clear=self._on_clear)
        self.layout.addWidget(self.actions_widget)

    def _build_result_widget(self) -> None:
        """Initialize PFM results display widget."""
        self.pfm_result_widget = PFMResultWidget(self.context, self.controller)
        self.layout.addWidget(self.pfm_result_widget)

    def _on_feature_selection_changed(self) -> None:
        """Update label and restrict maximum allowed factors."""
        super()._on_feature_selection_changed()
        count = len(self.feature_selector.get_selected_items())
        if count >= MIN_FEATURES:
            self.params_widget.set_max_factors(count - 1)
        self._refresh_buttons()

    def _on_data_changed(self, event: Event) -> None:
        """Refresh feature list and clear stale factor analysis results."""
        super()._on_data_changed(event)
        self._on_clear()
        if self._is_pca_space():
            update_status_label(
                self.status_label, 
                "Dataset is in PCA space. Restore original data in the PCA tab.", 
                ok=False
            )

    def _on_fit(self) -> None:
        """Fit Principal Factor Method model."""
        data = self._get_data(MIN_FEATURES)
        if data is None: 
            return
        df, selected_cols = data

        n_factors = self.params_widget.get_n_factors()
        h2_estimator = self.h2_widget.get_selected_estimator()

        try:
            self.controller.fit_transform(
                df[selected_cols], 
                h2_estimator_name=h2_estimator, 
                n_factors=n_factors,
            )
            self.pfm_result_widget.create_results()
            self._set_fit_status()
        except Exception as e:
            self.messenger.show_error("Fit failed", str(e))

    def _on_clear(self) -> None:
        """Clear controller state and PFM widget results."""
        self.controller.clear()
        self.pfm_result_widget.clear()
        update_status_label(self.status_label, "Results cleared", ok=True)

    def _refresh_buttons(self) -> None:
        """Refresh actions buttons enablement."""
        enabled = (len(self.feature_selector.get_selected_items()) >= MIN_FEATURES and not self._is_pca_space())
        self.actions_widget.set_fit_enabled(enabled)

    def _set_fit_status(self) -> None:
        """Display status of model convergence."""
        res = self.controller.get_results()
        result, ok = res["result"], res["ok"]
        update_status_label(
            self.status_label, 
            f"{result.value}, {res['n_iter']} iterations", 
            ok=ok
        )