from.max_corr_method import MaxCorrelationMethod
from .triads_method import TriadsMethod
from .averaging_method import AveragingMethod
from .centroid_method import CentroidMethod
from .averoid_method import AveroidMethod
from .pca_based_method import PCABasedMethod

from .base import BaseCommunalityEstimator

communality_estimators: list[BaseCommunalityEstimator] = [
    MaxCorrelationMethod(),
    TriadsMethod(),
    AveragingMethod(),
    CentroidMethod(),
    AveroidMethod(),
    PCABasedMethod(),
]