from typing import Callable
from dataclasses import dataclass
import pandas as pd

@dataclass
class GraphPanelCallbacks:
    set_data: Callable[[pd.Series], None]
    refresh_all: Callable[[], None]

def build_graph_panel_callbacks(panel) -> GraphPanelCallbacks:
    return GraphPanelCallbacks(
        set_data=lambda series: setattr(panel, 'data', series),
        refresh_all=panel.refresh_all
    )