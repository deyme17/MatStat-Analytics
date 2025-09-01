class SimulationController:
    """
    Main controller class for statistical simulation operations.
    """
    def __init__(self, simulation_service, data_saver):
        """
        Initialize the simulation controller with required services.
        Args:
            simulation_service: Service for performing statistical simulations
            data_saver: Service for saving simulated data to storage
        """
        self.simulation_service = simulation_service
        self.data_saver = data_saver
    
    def run_simulation(self, dist, sizes, repeats, true_mean, alpha,
                      save_data=False, sample_size=None):
        """Run statistical simulation with optional data saving.
        Args:
            dist: Distribution instance to simulate from
            sizes: List of sample sizes for the simulation experiment
            repeats: Number of repetitions per sample size
            true_mean: Theoretical mean to test against in t-tests
            alpha: Significance level for statistical tests
            save_data: Whether to save simulated data (default: False)
            sample_size: Size of sample to save if save_data is True
        Return:
            List of dictionaries containing simulation results
        """
        if save_data and sample_size and sample_size > 0:
            simulated_data = self.simulation_service.generate_sample(
                dist, sample_size, dist.params
            )
            self.data_saver.save_data(dist.name, simulated_data)
        
        return self.simulation_service.run_experiment(
            dist, sizes, repeats, true_mean, alpha
        )