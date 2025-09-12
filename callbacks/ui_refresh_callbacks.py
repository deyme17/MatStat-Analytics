from typing import Callable, Optional
import pandas as pd


class UIClearCallbacks:
    def __init__(
        self,
        clear_graph: Callable[[], None],
        clear_tables: Callable[[], None],
        clear_gof: Callable[[], None]
    ):
        self.clear_graph = clear_graph
        self.clear_tables = clear_tables
        self.clear_gof = clear_gof


class UIUpdateCallbacks:
    def __init__(
        self,
        set_graph_data: Callable[[Optional[pd.Series]], None],
        update_tables: Callable[[], None],
        evaluate_gof: Callable[[], None]
    ):
        self.set_graph_data = set_graph_data
        self.update_tables = update_tables
        self.evaluate_gof = evaluate_gof


class UIStateCallbacks:
    def __init__(
        self,
        update_state: Callable[[pd.Series], None],
        update_transformation_label: Callable[[], None],
        update_navigation_buttons: Callable[[], None],
        enable_original_button: Callable[[bool], None]
    ):
        self.update_state = update_state
        self.update_transformation_label = update_transformation_label
        self.update_navigation_buttons = update_navigation_buttons
        self.enable_original_button = enable_original_button


class UIModelCallbacks:
    def __init__(
        self,
        get_bins_count: Callable[[], int],
        update_model_bins: Optional[Callable[[int], None]] = None
    ):
        self.get_bins_count = get_bins_count
        self.update_model_bins = update_model_bins