import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

class Renderer(ABC):
    @abstractmethod
    def render(self, ax: plt.Axes, *args, **kwargs):
        pass