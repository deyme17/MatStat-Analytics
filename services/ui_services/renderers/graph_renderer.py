from abc import ABC, abstractmethod

class Renderer(ABC):
    @abstractmethod
    def render(self, ax, *args, **kwargs):
        pass