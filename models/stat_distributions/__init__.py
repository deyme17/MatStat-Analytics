from .normal import NormalDistribution
from .exponential import ExponentialDistribution
from .laplace import LaplaceDistribution
from .uniform import UniformDistribution
from .weibull import WeibullDistribution

from .stat_distribution import StatisticalDistribution

stat_distributions: list[type[StatisticalDistribution]] = [
    NormalDistribution,
    ExponentialDistribution,
    LaplaceDistribution,
    UniformDistribution,
    WeibullDistribution,
]