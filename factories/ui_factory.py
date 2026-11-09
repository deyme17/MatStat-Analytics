from .controllers_factory import Controllers
from dataclasses import dataclass
from typing import Callable
from utils import AppContext

# Services
from services import (
    ConfidenceAssesment, SimpleLinearRegression,
    StatsRenderer, VarSerRenderer, MultiVarRenderer,
    DataExporter,
)

# Views
from PyQt6.QtWidgets import QTabWidget, QWidget
from views import (
    # tabs
    DataProcessingTab, DistributionTab, SimulationTab, StatisticsTab, HomogenTab, CorrelationTab, RegressionTab,
    # widgets
    WindowWidgets,
    AnomalyWidget, MissingWidget, TransformDataWidget, PCAResultWidget, RegrSummaryWidget, RegrPredictionWidget,
    ParamEstimationWidget, GOFTestWidget, KolmogorovSmirnovPanel, PearsonChi2Panel, Pearson2DNormalPanel, 
    GenerationWidget, ExperimentWidget, CorrelationTestWidget, PartialCorrWidget, MultiCorrWidget, ComponentAnalysisTab,
    NormalHomogenPanel, WilcoxonPanel, MannWhitneyUPanel, RankMeanDiffPanel, SmirnovKolmogorovPanel, SignsCriterionPanel, 
    AbbePanel, ANOVAPanel, BurtlettPanel, CochranQPanel, HPanel, MultiNormalPanel,
    GraphPanel, DistributionSelector,
)
from views.tabs.graph_tabs import (
    EDFTab, HistogramTab, HHTab, 
    CorrelationFieldTab, HistogramMapTab,
    BubblePlotTab, CorreletionField3dTab,
    CorrelationMatrixTab, ScatterMatrixTab, 
    HeatMapTab, ParallelCoordsTab
)


@dataclass(frozen=True)
class TabSpec:
    attr: str                     # name of the attribute set on the window
    title: str                    # text shown on the tab
    build: Callable[[], QWidget]  # builder method


class UIFactory:
    def __init__(self, window, context: AppContext, controllers: Controllers):
        self.win = window
        self.context = context
        self.controllers = controllers

    def setup_ui(self) -> None:
        self.win.widgets = WindowWidgets.create_controls_bar()
        self.win.graph_panel = self._build_graph_panel()
        self._setup_left_tabs()

    def _tab_specs(self) -> list[TabSpec]:
        """
        Order here = order of the tabs in the window.
        To add a tab: write a _build_xxx_tab method and add one line.
        """
        return [
            TabSpec("data_tab",  "Data Processing",     self._build_data_tab),
            TabSpec("stat_tab",  "Statistics",          self._build_stat_tab),
            TabSpec("dist_tab",  "Distribution",        self._build_dist_tab),
            TabSpec("corr_tab",  "Correlation",         self._build_corr_tab),
            TabSpec("regr_tab",  "Regression",          self._build_regr_tab),
            TabSpec("comp_tab",  "Component-Factor",    self._build_comp_tab),
            TabSpec("homo_tab",  "Homogeneity Tests",   self._build_homo_tab),
            TabSpec("sim_tab",   "Simulation",          self._build_sim_tab),
        ]

    def _setup_left_tabs(self) -> None:
        tab_widget = QTabWidget()
        for spec in self._tab_specs():
            widget = spec.build()
            tab_widget.addTab(widget, spec.title)
            setattr(self.win, spec.attr, widget)
        self.win.left_tab_widget = tab_widget

    def _build_graph_panel(self) -> GraphPanel:
        ctx = self.context
        return GraphPanel(
            context=ctx,
            dist_selector=DistributionSelector(dist_register=self.controllers.dist_register),
            graph_tabs={
                "Histogram": HistogramTab(ctx),
                "EDF": EDFTab(ctx, ConfidenceAssesment()),
                "H-H Plot": HHTab(ctx),
                "3D Histogram Map": HistogramMapTab(ctx),
                "Correlation Field": CorrelationFieldTab(ctx, SimpleLinearRegression()),
                "Correlation Matrix": CorrelationMatrixTab(ctx, self.controllers.correlation),
                "Heatmap": HeatMapTab(ctx),
                "Scatter Matrix": ScatterMatrixTab(ctx),
                "Parallel Coordinates": ParallelCoordsTab(ctx),
                "Bubble Plot": BubblePlotTab(ctx),
                "Correletion Field 3D": CorreletionField3dTab(ctx),
            },
        )

    def _build_data_tab(self) -> DataProcessingTab:
        return DataProcessingTab(
            context=self.context,
            dataset_controller=self.controllers.data_version,
            data_exporter=DataExporter,
            widget_data=[
                ("transform_widget", TransformDataWidget, self.controllers.data_transform),
                ("anomaly_widget", AnomalyWidget, self.controllers.anomaly_data),
                ("missing_widget", MissingWidget, self.controllers.missing_data),
            ],
        )

    def _build_stat_tab(self) -> StatisticsTab:
        return StatisticsTab(
            stat_renderer_cls=StatsRenderer,
            var_renderer_cls=VarSerRenderer,
            multi_renderer_cls=MultiVarRenderer,
        )

    def _build_dist_tab(self) -> DistributionTab:
        return DistributionTab(
            dist_register=self.controllers.dist_register,
            param_estimation_widget=ParamEstimationWidget(
                context=self.context,
                estimator=self.controllers.estimation,
            ),
            gof_tests_widget=GOFTestWidget(
                context=self.context,
                gof_controller=self.controllers.gof,
                test_panels=[PearsonChi2Panel, KolmogorovSmirnovPanel],
                multi_test_panels=[Pearson2DNormalPanel],
            ),
        )

    def _build_corr_tab(self) -> CorrelationTab:
        return CorrelationTab(
            context=self.context,
            corr_controller=self.controllers.correlation,
            corr_test_widget=CorrelationTestWidget,
            partial_corr_widget=PartialCorrWidget,
            multi_corr_widget=MultiCorrWidget,
        )

    def _build_regr_tab(self) -> RegressionTab:
        return RegressionTab(
            context=self.context,
            regr_controller=self.controllers.regression,
            summary_widget=RegrSummaryWidget,
            prediction_widget=RegrPredictionWidget,
        )

    def _build_comp_tab(self) -> ComponentAnalysisTab:
        return ComponentAnalysisTab(
            context=self.context,
            component_controller=self.controllers.component,
            pca_result_widget=PCAResultWidget,
        )

    def _build_homo_tab(self) -> HomogenTab:
        return HomogenTab(
            homogen_controller=self.controllers.homogen,
            context=self.context,
            homogen_2samples_panels=[
                NormalHomogenPanel, WilcoxonPanel, MannWhitneyUPanel,
                RankMeanDiffPanel, SmirnovKolmogorovPanel, SignsCriterionPanel,
            ],
            homogen_Nsamples_panels=[
                ANOVAPanel, BurtlettPanel, CochranQPanel, HPanel, MultiNormalPanel,
            ],
            hamogen_1sample_panels=[AbbePanel],
        )

    def _build_sim_tab(self) -> SimulationTab:
        return SimulationTab(
            messanger=self.context.messanger,
            simulation_controller=self.controllers.simulation,
            dist_register=self.controllers.dist_register,
            experiment_widget=ExperimentWidget,
            generation_widget=GenerationWidget,
        )
