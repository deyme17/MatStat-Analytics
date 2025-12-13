from .interfaces import IRegression
from .regression_models import LinearRegression, PolynomialRegression
from .algorithms import OLS

regression_models: list[IRegression] = [
    LinearRegression(algorithm=OLS()),
    PolynomialRegression(algorithm=OLS(),
                         degree=2),
    PolynomialRegression(algorithm=OLS(),
                         degree=3)
]