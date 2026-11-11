from .homodata_selector import HomoDataSelectorWidget
from .homotest_section_group import HomoTestSectionGroup
from .panels.homogen_panel import BaseHomoTestPanel

from .panels.two_samples_panels.normal_homogen_panel import NormalHomogenPanel
from .panels.two_samples_panels.wilcoxon_panel import WilcoxonPanel
from .panels.two_samples_panels.mann_whitney_U_panel import MannWhitneyUPanel
from .panels.two_samples_panels.rank_mean_diff_panel import RankMeanDiffPanel
from .panels.two_samples_panels.smirnov_kolmogorov_panel import SmirnovKolmogorovPanel
from .panels.two_samples_panels.signs_criterion_panel import SignsCriterionPanel

from .panels.n_samples_panels.bartlett_panel import BurtlettPanel
from .panels.n_samples_panels.anova_panel import ANOVAPanel
from .panels.n_samples_panels.cochran_Q_panel import CochranQPanel
from .panels.n_samples_panels.kruskal_wallis_H_panel import HPanel
from .panels.n_samples_panels.multivariate_normal_panel import MultiNormalPanel

from .panels.one_sample_panels.abbe_panel import AbbePanel