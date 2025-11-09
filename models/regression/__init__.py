from .regression_model import IRegression
from .linear_regression import LinearRegression

from services import OLS

regression_models: list[IRegression] = [
    LinearRegression(algorithm=OLS())
]