class SimulationController:
    """
    Main controller class for statistical simulation operations.
    """
    def __init__(self, simulation_service, data_saver):
        """
        Initialize the simulation controller with required services.
        :param simulation_service: Service for performing statistical simulations
        :param data_saver: Service for saving simulated data to storage
        """
        self.simulation_service = simulation_service
        self.data_saver = data_saver
    
    def run_simulation(self, dist, sizes, repeats, true_mean, alpha,
                      save_data=False, sample_size=None):
        """Run statistical simulation with optional data saving.
        
        :param dist: Distribution instance to simulate from
        :param sizes: List of sample sizes for the simulation experiment
        :param repeats: Number of repetitions per sample size
        :param true_mean: Theoretical mean to test against in t-tests
        :param alpha: Significance level for statistical tests
        :param save_data: Whether to save simulated data (default: False)
        :param sample_size: Size of sample to save if save_data is True
        :return: List of dictionaries containing simulation results
        """
        if save_data and sample_size:
            simulated_data = self.simulation_service.generate_sample(
                dist, sample_size, dist.params
            )
            self.data_saver.save_data(dist.name, simulated_data)
        
        return self.simulation_service.run_experiment(
            dist, sizes, repeats, true_mean, alpha
        )