from .normal import NormalDistribution
from .exponential import ExponentialDistribution
from .laplace import LaplaceDistribution
from .uniform import UniformDistribution
from .weibull import WeibullDistribution

from .stat_distribution import StatisticalDistribution

registered_distributions: dict[str, StatisticalDistribution] = {
    "Normal": NormalDistribution,
    "Exponential": ExponentialDistribution,
    "Laplace": LaplaceDistribution,
    "Uniform": UniformDistribution,
    "Weibull": WeibullDistribution,
}
