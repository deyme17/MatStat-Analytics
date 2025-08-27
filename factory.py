# Controllers
from controllers import (
    AnomalyController, MissingDataController, DataTransformController,
    ParameterEstimation, SimulationController, StatisticController,
    DataLoadController, DataVersionController,
    GraphController, UIStateController
)

# Services
from services import (
    TransformationService, AnomalyService, MissingService,
    ConfidenceService, GOFService, TestPerformer, StatisticsService,
    UIRefreshService, UIMessager, MissingInfoDisplayService, TableRenderer,
    DataHistoryManager, DataLoaderService,
    SimulationService, DataSaver
)

# Views
from PyQt6.QtWidgets import QTabWidget
from views import (
    # tabs
    DataProcessingTab, GOFTestTab, ParamEstimationTab, SimulationTab, StatisticTab,
    # widgets
    WindowWidgets,
    AnomalyWidget, MissingWidget, ProcessDataWidget,
    KolmogorovSmirnovPanel, PearsonChi2Panel,
    GraphPanel, DistributionSelector
)

# Callbacks
from callbacks import UIClearCallbacks, UIUpdateCallbacks, UIModelCallbacks, UIStateCallbacks
from callbacks.ui_state_callbacks import build_ui_control_callbacks


class Factory:
    @staticmethod
    def create(window, context):
        Factory._setup_controls(window)
        Factory._setup_graph(window, context)
        Factory._setup_services(window, context)
        Factory._setup_controllers(window, context)
        Factory._setup_tabs(window, context)

    @staticmethod
    def _setup_controls(window):
        widgets = WindowWidgets()
        controls = widgets.create_controls_bar()

        window.load_data_button = controls.load_button
        window.precision_spinbox = controls.precision_spinbox
        window.controls_layout = controls.layout

    @staticmethod
    def _setup_services(window, context):
        context.version_manager = DataHistoryManager()
        context.message_service = UIMessager(parent=window)

        # Instantiate callback groups
        clear_callbacks = UIClearCallbacks(
            clear_graph=window.graph_panel.clear,
            clear_stats=window.stat_controller.clear,
            clear_gof=window.gof_tab.clear_panels
        )

        update_callbacks = UIUpdateCallbacks(
            set_graph_data=lambda data: (
                setattr(window.graph_panel, 'data', data) if data is None
                else window.graph_controller.set_data(data)
            ),
            update_stats=window.stat_controller.update_statistics_table,
            evaluate_gof=window.gof_tab.evaluate_tests
        )

        state_callbacks = UIStateCallbacks(
            update_state=window.state_controller.update_state_for_data,
            update_transformation_label=window.state_controller.update_transformation_label,
            update_navigation_buttons=window.state_controller.update_navigation_buttons,
            enable_original_button=window.original_button.setEnabled
        )

        model_callbacks = UIModelCallbacks(
            get_bins_count=lambda: window.graph_panel.bins_spinbox.value(),
            update_model_bins=lambda bins: (
                window.data_model.update_bins(bins) if window.data_model else None
            )
        )

        # Instantiate UIRefreshService with callback groups
        context.refresher = UIRefreshService(
            clear=clear_callbacks,
            update=update_callbacks,
            state=state_callbacks,
            model=model_callbacks
        )

        context.data_model = None

    @staticmethod
    def _setup_graph(window, context):
        graph_panel = GraphPanel(
            dist_selector_cls=DistributionSelector
        )
        window.graph_panel = graph_panel
        context.graph_panel = graph_panel

    @staticmethod
    def _setup_controllers(window, context):
        window.graph_controller = GraphController(
            context=context,
            panel=window.graph_panel,
            confidence_service=ConfidenceService(),
            update_statistics_callback=lambda: window.stat_controller.update_statistics_table() if hasattr(window, 'stat_controller') else None,
            update_gof_callback=lambda: window.gof_tab.evaluate_tests() if hasattr(window, 'gof_tab') else None
        )
        # set graph_panel callbacks
        window.graph_panel.set_callbacks(
            on_bins_changed=window.graph_controller.on_bins_changed,
            on_alpha_changed=window.graph_controller.on_alpha_changed,
            on_kde_toggled=window.graph_controller.on_kde_toggled,
            on_dist_changed=window.graph_controller.on_distribution_changed
        )

        window.transform_controller = DataTransformController(
            context=context,
            transform_service=TransformationService(),
            shift_spinbox=window.shift_spinbox,
            on_transformation_applied=lambda: window.original_button.setEnabled(True)
        )

        window.data_version_controller = DataVersionController(
            context=context,
            data_version_combo=window.data_version_combo,
            bins_spinbox=window.graph_panel.bins_spinbox,
            on_reverted_to_original=lambda: window.original_button.setEnabled(False),
            on_version_changed=lambda series: window.missing_controller.update_data_reference(series)
        )

        window.missing_controller = MissingDataController(
            context=context,
            missing_service=MissingService(),
            display_service=MissingInfoDisplayService(
                    count_label=window.missing_count_label,
                    percent_label=window.missing_percentage_label
            ),
            update_state_callback=window.state_controller.update_state_for_data
        )

        window.anomaly_controller = AnomalyController(
            context=context,
            anomaly_service=AnomalyService(),
            gamma_spinbox=window.anomaly_gamma_spinbox.value()
        )

        window.stat_controller = StatisticController(
            data_model=context.data_model,
            graph_panel=context.graph_panel,
            precision_spinbox=window.precision_spinbox,
            bins_spinbox=window.graph_panel.bins_spinbox,
            stat_table_widget=window.stat_tab.conf_table if hasattr(window, "stat_tab") else None,
            statistic_service=StatisticsService(),
            stats_renderer=TableRenderer()
        )

        window.state_controller = UIStateController(
            context=context,
            missing_service=MissingService(),
            data_version_combo=window.data_version_combo,
            ui_controls=build_ui_control_callbacks(window),
            update_data_callback=lambda data: window.missing_controller.update_data_reference(data)
        )

        window.data_load_controller = DataLoadController(
            context=context,
            loader_service=DataLoaderService(),
            select_file_callback=lambda: DataLoaderService.select_file(window),
            on_data_loaded_callback=lambda data: (
                window.state_controller.handle_post_load_state(data),
                window.original_button.setEnabled(False)
            )
        )

    @staticmethod
    def _setup_tabs(window, context):
        window.data_tab = DataProcessingTab(
            window,
            dp_widgets=[
                ProcessDataWidget,
                AnomalyWidget,
                MissingWidget
            ]
        )

        window.stat_tab = StatisticTab()

        window.gof_tab = GOFTestTab(
            context=context,
            graph_panel=context.graph_panel,
            gof_service=GOFService(),
            test_panels=[PearsonChi2Panel, KolmogorovSmirnovPanel]
        )

        window.sim_tab = SimulationTab(
            context=context,
            simulation_controller=SimulationController(
                simulation_service=SimulationService(test_performer=TestPerformer()),
                data_saver=DataSaver(context, on_save=lambda data: window.state_controller.handle_post_load_state(data))
            )
        )

        window.est_tab = ParamEstimationTab(
            context=context,
            estimator=ParameterEstimation()
        )

        window.left_tab_widget = QTabWidget()
        window.left_tab_widget.addTab(window.data_tab, "Data Processing")
        window.left_tab_widget.addTab(window.stat_tab, "Statistic")
        window.left_tab_widget.addTab(window.gof_tab, "Goodness-of-Fit Tests")
        window.left_tab_widget.addTab(window.sim_tab, "Simulation")
        window.left_tab_widget.addTab(window.est_tab, "Parameters estimation")