from .normal_homogen_test import NormalHomogenTest
from .wilcoxon_test import WilcoxonTest
from .mann_whitney_U_test import MannWhitneyUTest
from .rank_mean_diff_test import RankMeanDiffTest
from .smirnov_kolmogorov_test import SmirnovKolmogorovTest
from .signs_criterion_test import SignsCriterionTest

homogens_tests = [
    NormalHomogenTest,
    WilcoxonTest,
    MannWhitneyUTest,
    RankMeanDiffTest,
    SmirnovKolmogorovTest,
    SignsCriterionTest,
]