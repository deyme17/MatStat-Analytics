from .normal_homogen_test import NormalHomogenTest
from .wilcoxon_homogen_test import WilcoxonHomogenTest
from .mann_whitney_U_test import MannWhitneyUTest
from .rank_mean_diff_test import RankMeanDiffTest

homogens_tests = [
    NormalHomogenTest,
    WilcoxonHomogenTest,
    MannWhitneyUTest,
    RankMeanDiffTest,
]