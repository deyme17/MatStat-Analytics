from models.params_estimators.maximum_likelihood import MaximumLikelihoodMethod
from models.params_estimators.method_of_moments import MethodOfMoments
from .base import BaseEstimationMethod

estimation_methods: list[BaseEstimationMethod] = [
    MethodOfMoments(),
    MaximumLikelihoodMethod()
]