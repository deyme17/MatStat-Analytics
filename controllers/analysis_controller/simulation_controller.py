from services import SimulationService, DataSaver, DataExporter, DataVersionManager, UIMessager
from models.stat_distributions.stat_distribution import StatisticalDistribution
from utils import AppContext, EventType, EventBus


class SimulationController:
    """
    Main controller class for statistical simulation operations.
    """
    def __init__(self, context: AppContext, simulation_service: SimulationService, data_saver: DataSaver, data_exporter: DataExporter):
        """
        Args:
            simulation_service: Service for performing statistical simulations
            data_saver: Service for saving simulated data to storage
            data_exporter: Service for exporting simulated data as csv
        """
        self.simulation_service: SimulationService = simulation_service
        self.data_saver: DataSaver = data_saver
        self.data_exporter: DataExporter = data_exporter
        self.context: AppContext = context
        self.version_manager: DataVersionManager = context.version_manager
        self.event_bus: EventBus = context.event_bus
        self.messanger: UIMessager = context.messanger
    
    def run_simulation(self, dist: StatisticalDistribution, sizes: list[int], repeats: int, true_mean: float, alpha: float):
        """
        Run statistical simulation with optional data saving.
        Args:
            dist: Distribution instance to simulate from
            sizes: List of sample sizes for the simulation experiment
            repeats: Number of repetitions per sample size
            true_mean: Theoretical mean to test against in t-tests
            alpha: Significance level for statistical tests
        Return:
            List of dictionaries containing simulation results
        """
        try:
            return self.simulation_service.run_experiment(
                dist, sizes, repeats, true_mean, alpha
            )
        except Exception as e:
            self.messanger.show_info(f"Simulation error: {str(e)}")
            return []
        
    def generate_data(self, dist: StatisticalDistribution, n_features: int, coors_coeffs: list[list[float]],
                      sample_size: int, export_data: bool = False) -> None:
        """
        Generate simulated data from statistical distribution with optional export.
        Args:
            dist: Statistical distribution instance to simulate data from
            n_features: Number of features/dimensions in the generated dataset
            coors_coeffs: Correlation coefficients matrix defining feature relationships
            sample_size: Number of samples/observations to generate
            export_data: Whether to export generated data to external file
        """
        try:
            simulated_data = None
            if sample_size and sample_size > 0:
                simulated_data = self.simulation_service.generate_data(
                    dist, n_features, coors_coeffs, sample_size, dist.params
                )
            if simulated_data is not None and len(simulated_data) > 0:
                data_model = self.data_saver.save_data(dist.name, simulated_data)
                self.version_manager.add_dataset(data_model.label, data_model)
                self.context.data_model = data_model
                self.event_bus.emit_type(EventType.DATA_LOADED, data_model.series)
                self.messanger.show_info(
                    "Data Saved", 
                    f"Simulated data saved as '{data_model.label}' with {len(simulated_data)} samples."
                )
                if export_data:
                    filepath = self.data_exporter.export(dist.name, simulated_data)
                    self.messanger.show_info(
                        "Data Exported", 
                        f"Simulated data saved in '{filepath}' with {len(simulated_data)} samples."
                    )
            elif sample_size and sample_size > 0:
                self.messanger.show_info(f"Warning: Could not generate data for {dist.name}")
        except Exception as e:
            self.messanger.show_info(f"Simulation error: {str(e)}")
            return