from .two_samples_tests.normal_homogen_test import NormalHomogenTest
from .two_samples_tests.wilcoxon_test import WilcoxonTest
from .two_samples_tests.mann_whitney_U_test import MannWhitneyUTest
from .two_samples_tests.rank_mean_diff_test import RankMeanDiffTest
from .two_samples_tests.smirnov_kolmogorov_test import SmirnovKolmogorovTest
from .two_samples_tests.signs_criterion_test import SignsCriterionTest

from .one_sample_tests.abbe_test import AbbeTest

from .n_samples_tests.bartlett_test import BartlettTest
from .n_samples_tests.anova_test import ANOVATest
from .n_samples_tests.cochran_Q_test import CochranQTest
from .n_samples_tests.kruskal_wallis_H_test import HTest

from .base_homogen_test import BaseHomogenTest

homogens_tests: list[BaseHomogenTest] = [
    NormalHomogenTest,
    WilcoxonTest,
    MannWhitneyUTest,
    RankMeanDiffTest,
    SmirnovKolmogorovTest,
    SignsCriterionTest,

    BartlettTest,
    ANOVATest,
    CochranQTest,
    HTest,

    AbbeTest
]