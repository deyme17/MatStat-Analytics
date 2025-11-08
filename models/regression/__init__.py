from .regression_model import IRegression
from .linear_regression import LinearRegression

regression_models: list[type[IRegression]] = [
    LinearRegression
]