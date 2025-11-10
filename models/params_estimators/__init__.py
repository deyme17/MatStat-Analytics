from models.params_estimators.maximum_likelihood import MaximumLikelihoodMethod
from models.params_estimators.method_of_moments import MethodOfMoments
from .base_method import EstimationMethod

estimation_methods: list[EstimationMethod] = [
    MethodOfMoments(),
    MaximumLikelihoodMethod()
]