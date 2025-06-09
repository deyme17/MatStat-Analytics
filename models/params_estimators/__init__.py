from models.params_estimators.maximum_likelihood import MaximumLikelihoodMethod
from models.params_estimators.method_of_moments import MethodOfMoments

registered_estimation_methods = {
    MethodOfMoments().name: MethodOfMoments(),
    MaximumLikelihoodMethod().name: MaximumLikelihoodMethod()
}