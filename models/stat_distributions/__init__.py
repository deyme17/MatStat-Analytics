from .normal import NormalDistribution
from .exponential import ExponentialDistribution
from .laplace import LaplaceDistribution
from .uniform import UniformDistribution
from .weibull import WeibullDistribution

from .base import BaseDistribution

stat_distributions: list[type[BaseDistribution]] = [
    NormalDistribution,
    ExponentialDistribution,
    LaplaceDistribution,
    UniformDistribution,
    WeibullDistribution,
]