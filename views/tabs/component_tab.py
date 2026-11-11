from views.widgets.utils.base_analysis_tab import BaseAnalysisTab
from views.widgets.componentwidgets import PCAResultWidget, PCAParamsWidget, PCAActionsWidget
from services.ui_services.renderers.graph_renderers import ScreeEVRPlot
from controllers import ComponentController
from controllers.analysis_controllers.component_controller import PCAState
from views.widgets.utils import update_status_label
from utils import AppContext, Event

MIN_FEATURES = 2


class ComponentTab(BaseAnalysisTab):
    """Component analysis tab that implements Principal Component Analysis."""
    def __init__(self, context: AppContext, component_controller: ComponentController):
        """
        Args:
            context: Shared application context (data_model, event_bus, messager).
            component_controller: Controller for performing component analysis.
        """
        self.controller: ComponentController = component_controller
        super().__init__(context, title="PCA Config")
        self._refresh_buttons()

    def _build_custom_ui(self) -> None:
        """Build parameters and action widgets for PCA."""
        self.params_widget = PCAParamsWidget()
        self.layout.addWidget(self.params_widget)

        callbacks = {
            "fit": self._on_fit,
            "transform": self._on_transform,
            "scree": self._on_scree_plot,
            "inverse": self._on_inverse_transform,
            "original": self._on_to_original
        }
        self.actions_widget = PCAActionsWidget(callbacks)
        self.layout.addWidget(self.actions_widget)

    def _build_result_widget(self) -> None:
        """Initialize PCA results display widget."""
        self.pca_result_widget = PCAResultWidget(self.context, self.controller)
        self.layout.addWidget(self.pca_result_widget)

    def _on_feature_selection_changed(self) -> None:
        """Update label and restrict max n_components based on selected feature count."""
        super()._on_feature_selection_changed()
        count = len(self.feature_selector.get_selected_items())
        if count >= MIN_FEATURES:
            self.params_widget.set_max_components(count)

    def _on_data_changed(self, event: Event) -> None:
        """Refresh feature list and button states whenever data changes."""
        super()._on_data_changed(event)
        self._refresh_buttons()

    def _on_fit(self) -> None:
        """Fit Principal Component Analysis model on selected features."""
        data = self._get_data(MIN_FEATURES)
        if data is None: 
            return
        df, selected_cols = data

        try:
            self.controller.fit(df[selected_cols])
            self.pca_result_widget.create_results()
            self._refresh_buttons()
            update_status_label(self.status_label, "Model fitted successfully", ok=True)
        except Exception as e:
            self.messenger.show_error("Fit failed", str(e))

    def _on_transform(self) -> None:
        """Transform dataset using fitted PCA model."""
        data = self._get_data(MIN_FEATURES)
        if data is None: 
            return
        df, selected_cols = data

        n_components, ev_threshold = self.params_widget.get_params()
        state = self.controller.current_state
        current_dataset = self.context.version_manager.get_current_dataset_name()
        fit_needed = (state == PCAState.IDLE or self.controller.fitted_ds_name != current_dataset)

        try:
            self.controller.transform(df[selected_cols], df, fit_needed, n_components, ev_threshold)
            self.pca_result_widget.create_results()
            self._refresh_buttons()
            update_status_label(self.status_label, f"Transformed to {n_components or 'auto'} components", ok=True)
        except Exception as e:
            self.messenger.show_error("Transform failed", str(e))

    def _on_scree_plot(self) -> None:
        """Open Scree Plot visualization dialog."""
        try:
            _, evr = self.controller.get_explained_variance()
            dialog = ScreeEVRPlot(evr, parent=self)
            dialog.exec()
        except Exception as e:
            self.messenger.show_error("Scree plot failed", str(e))

    def _on_inverse_transform(self) -> None:
        """Apply inverse transform to reconstructed space."""
        df = self.context.data_model.dataframe
        if df is None:
            return
        try:
            self.controller.inverse_transform(df)
            self._refresh_buttons()
            update_status_label(self.status_label, "Data inverse-transformed", ok=True)
        except Exception as e:
            self.messenger.show_error("Inverse transform failed", str(e))

    def _on_to_original(self) -> None:
        """Revert data to original feature space."""
        try:
            self.controller.to_original()
            self.pca_result_widget.refresh()
            self._refresh_buttons()
            update_status_label(self.status_label, "Restored original data", ok=True)
        except Exception as e:
            self.messenger.show_error("Restore failed", str(e))

    def _refresh_buttons(self) -> None:
        """Update interactive buttons enablement depending on current PCA state."""
        state = self.controller.current_state
        current_dataset = self.context.version_manager.get_current_dataset_name()
        fitted_here = self.controller.fitted_ds_name == current_dataset
        has_enough_features = len(self.feature_selector.get_selected_items()) >= MIN_FEATURES

        state_str = "transformed" if state == PCAState.TRANSFORMED else ("fitted" if state == PCAState.FITTED else "idle")
        is_inverse = (state == PCAState.INVERSE_TRANSFORMED)

        self.actions_widget.update_states(has_enough_features, state_str, fitted_here, is_inverse)