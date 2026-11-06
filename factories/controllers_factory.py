from functools import partial
from dataclasses import dataclass
from utils.app_context import AppContext

# Services
from services import (
    TestPerformer, DataLoaderService, DataSaver, DataExporter
)

# Models
from models import (
    stat_distributions, estimation_methods, gof_tests, 
    homogen_tests, regression_models, corr_coeffs, 
    StatisticsCalculator, MultipleCorrelation, PartialCorrelation,
    TransformationProcessor, AnomalyProcessor, MissingProcessor,
    SimulationEngine, PCA,
)

# Controllers
from controllers import (
    AnomalyController, MissingDataController, DataTransformController, StatisticsController, 
    EstimationController, GOFController, HomogenController, SimulationController,
    CorrelationController, RegressionController, ComponentController,
    DataLoadController, DatasetController, DistributionRegister,
)


@dataclass
class Controllers:
    statistics: StatisticsController
    data_loader: DataLoadController
    simulation: SimulationController
    estimation: EstimationController
    gof: GOFController
    homogen: HomogenController
    data_version: DatasetController
    anomaly_data: AnomalyController
    data_transform: DataTransformController
    missing_data: MissingDataController
    correlation: CorrelationController
    regression: RegressionController
    dist_register: DistributionRegister
    component: ComponentController



class ControllersFactory:
    def __init__(self, window, context: AppContext):
        self.window = window
        self.context = context

    def create(self) -> Controllers:
        """Initialize all controllers with no UI dependencies."""
        return Controllers(
            statistics=StatisticsController(
                context=self.context,
                stat_calculator=StatisticsCalculator(),
            ),
            data_loader=DataLoadController(
                context=self.context,
                loader_service=DataLoaderService(),
                select_file_callback=partial(DataLoaderService.select_file, self.window),
            ),
            simulation=SimulationController(
                context=self.context,
                simulation_engine=SimulationEngine(TestPerformer()),
                data_saver=DataSaver(),
                data_exporter=DataExporter,
            ),
            estimation=EstimationController(estimation_methods),
            gof=GOFController(gof_tests),
            homogen=HomogenController(homogen_tests),
            data_version=DatasetController(context=self.context),
            anomaly_data=AnomalyController(
                context=self.context,
                anomaly_proc=AnomalyProcessor(),
            ),
            data_transform=DataTransformController(
                context=self.context,
                transform_proc=TransformationProcessor(),
            ),
            missing_data=MissingDataController(
                context=self.context,
                missing_proc=MissingProcessor(),
            ),
            correlation=CorrelationController(
                corr_coeffs,
                partial_corr_cls=PartialCorrelation,
                multiple_corr_cls=MultipleCorrelation,
            ),
            regression=RegressionController(regression_models),
            dist_register=DistributionRegister(stat_distributions),
            component=ComponentController(context=self.context, pca=PCA()),
        )