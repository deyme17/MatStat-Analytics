from services.ui_services.renderers.hist_renderer import HistRenderer
from services.ui_services.renderers.edf_renderer import EDFRenderer
from services.ui_services.renderers.dist_renderer import DistributionRenderer

RENDERERS = {
    'histogram': HistRenderer,
    'edf': EDFRenderer,
    'distribution': DistributionRenderer
}