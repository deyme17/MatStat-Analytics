from .normal import NormalDistribution
from .exponential import ExponentialDistribution
from .laplace import LaplaceDistribution
from .uniform import UniformDistribution
from .weibull import WeibullDistribution

registered_distributions = {
    "Normal": NormalDistribution,
    "Exponential": ExponentialDistribution,
    "Laplace": LaplaceDistribution,
    "Uniform": UniformDistribution,
    "Weibull": WeibullDistribution,
}
