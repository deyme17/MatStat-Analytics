from services import DataSaver, DataExporter, DataVersionManager, UIMessager
from models import SimulationEngine
from models.stat_distributions.stat_distribution import StatisticalDistribution
from utils import AppContext, EventType, EventBus
from typing import Optional, List, Tuple


class SimulationController:
    """
    Main controller class for statistical simulation operations.
    """
    def __init__(self, context: AppContext, simulation_engine: SimulationEngine, data_saver: DataSaver, data_exporter: DataExporter):
        """
        Args:
            simulation_engine: Class for performing statistical simulations
            data_saver: Service for saving simulated data to storage
            data_exporter: Service for exporting simulated data as csv
        """
        self.simulation_engine: SimulationEngine = simulation_engine
        self.data_saver: DataSaver = data_saver
        self.data_exporter: DataExporter = data_exporter
        self.context: AppContext = context
        self.version_manager: DataVersionManager = context.version_manager
        self.event_bus: EventBus = context.event_bus
        self.messanger: UIMessager = context.messanger
    
    def run_experiment(self, dist: StatisticalDistribution, sizes: List[int], repeats: int, true_mean: float, alpha: float):
        """
        Run statistical experiment with optional data saving.
        Args:
            dist: Distribution instance to simulate from
            sizes: List of sample sizes for the simulation experiment
            repeats: Number of repetitions per sample size
            true_mean: Theoretical mean to test against in t-tests
            alpha: Significance level for statistical tests
        Return:
            List of dictionaries containing experiment results
        """
        try:
            return self.simulation_engine.run_experiment(
                dist, sizes, repeats, true_mean, alpha
            )
        except Exception as e:
            self.messanger.show_info("Simulation error", f"{str(e)}")
            return []
        
    def generate_data(self, distribution: StatisticalDistribution, n_features: int,
                      params_list: List[Tuple], coor_coeffs: Optional[List[List[float]]],
                      sample_size: int, export_data: bool = False) -> None:
        """
        Generate simulated data from statistical distribution with optional export.
        Args:
            distribution: instance of StatisticalDistribution
            params_list: List of parameters for each feature
            n_features: Number of features/dimensions in the generated dataset
            coor_coeffs: Correlation coefficients matrix defining feature relationships
            sample_size: Number of samples/observations to generate
            export_data: Whether to export generated data to external file
        """
        try:
            simulated_data = None
            if sample_size and sample_size > 0:
                simulated_data = self.simulation_engine.generate_data(
                    distribution, n_features, params_list, coor_coeffs, sample_size
                )
            if simulated_data is not None and len(simulated_data) > 0:
                data_model = self.data_saver.save_data(distribution.name, simulated_data)
                self.version_manager.add_dataset(data_model.label, data_model)
                self.context.data_model = data_model
                self.event_bus.emit_type(EventType.DATA_LOADED, data_model.series)
                self.messanger.show_info(
                    "Data Saved", 
                    f"Simulated data saved as '{data_model.label}' with {len(simulated_data)} samples."
                )
                if export_data:
                    filepath = self.data_exporter.export(distribution.name, simulated_data)
                    self.messanger.show_info(
                        "Data Exported", 
                        f"Simulated data saved in '{filepath}' with {len(simulated_data)} samples."
                    )
            elif sample_size and sample_size > 0:
                self.messanger.show_info("Warning", f"Could not generate data for {distribution.name}")
        except Exception as e:
            self.messanger.show_info("Simulation error", f"{str(e)}")
            return