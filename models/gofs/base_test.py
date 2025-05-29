from abc import ABC, abstractmethod

class BaseGOFTest(ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def run(self, data, dist, **kwargs):
        pass