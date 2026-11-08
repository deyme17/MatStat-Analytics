from abc import ABC, abstractmethod

class BaseGOFTest(ABC):
    """Abstract base class for goodness-of-fit test."""
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def run(self, data, dist, **kwargs):
        pass