from .corr_coeff import ICorrelationCoefficient
from .pearson_corr_coef import PearsonCorrelation
from .spearman_corr_coeff import SpearmanCorrelation
from .kendall_corr_coeff import KendallCorrelation
from .ratio_corr_coef import CorrelationRatio

corr_coefs: list[type[ICorrelationCoefficient]] = [
    PearsonCorrelation,
    SpearmanCorrelation,
    KendallCorrelation,
    CorrelationRatio
]