from .interfaces import IRegression
from .regression_models import LinearRegression
from .algorithms import OLS

regression_models: list[IRegression] = [
    LinearRegression(algorithm=OLS())
]