from .base import BaseCorrelationCoefficient
from .pearson_corr_coef import PearsonCorrelation
from .spearman_corr_coeff import SpearmanCorrelation
from .kendall_corr_coeff import KendallCorrelation
from .ratio_corr_coef import CorrelationRatio

from .partial_corr_coeff import PartialCorrelation
from .multiple_corr_coeff import MultipleCorrelation

corr_coeffs: list[BaseCorrelationCoefficient] = [
    PearsonCorrelation(),
    SpearmanCorrelation(),
    KendallCorrelation(),
    CorrelationRatio(),
]