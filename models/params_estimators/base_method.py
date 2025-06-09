from abc import ABC, abstractmethod
import pandas as pd

class EstimationMethod(ABC):
    @abstractmethod
    def estimate(self, dist_instance, data: pd.Series) -> tuple | None:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass
