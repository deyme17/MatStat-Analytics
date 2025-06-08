from services.ui_services.renderers.graph_renderers.hist_renderer import HistRenderer
from services.ui_services.renderers.graph_renderers.edf_renderer import EDFRenderer
from services.ui_services.renderers.graph_renderers.dist_renderer import DistributionRenderer

RENDERERS = {
    'histogram': HistRenderer,
    'edf': EDFRenderer,
    'distribution': DistributionRenderer
}