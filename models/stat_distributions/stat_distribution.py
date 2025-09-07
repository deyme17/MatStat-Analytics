from abc import ABC, abstractmethod
import numpy as np
import pandas as pd

class StatisticalDistribution(ABC):
    """Abstract base class for statistical distributions."""
    def __init__(self):
        self.params = None                     # parameters of the distribution
        self.color = 'red'                     # default color
        self.name = self.__class__.__name__    # name of the distribution

    @property
    @abstractmethod
    def distribution_params(self) -> dict[str, float | None]:
        pass

    @abstractmethod
    def fit(self, data: pd.Series) -> tuple:
        pass

    @abstractmethod
    def validate_params(self) -> bool:
        pass

    @abstractmethod
    def get_pdf(self, x: np.ndarray, params: tuple) -> np.ndarray:
        pass

    @abstractmethod
    def get_cdf_variance(self, x_vals: np.ndarray, params: tuple, n: int) -> np.ndarray:
        pass

    @abstractmethod
    def get_inverse_cdf(self, x: np.ndarray, params: tuple) -> np.ndarray:
        pass

    @abstractmethod
    def get_mean(self) -> float:
        pass

    def get_distribution_object(self, params: tuple):
        return None

    def get_plot_data(self, data: pd.Series, params: tuple) -> tuple[np.ndarray, np.ndarray]:
        x_min, x_max = self._get_plot_range(data)
        x = np.linspace(x_min, x_max, 1000)
        pdf = self.get_pdf(x, params)
        return x, pdf

    def _get_plot_range(self, data: pd.Series) -> tuple[float, float]:
        min_val = np.nanmin(data)
        max_val = np.nanmax(data)
        return min_val * 0.8, max_val * 1.2

    def __str__(self) -> str:
        return f"{self.name} Distribution"
