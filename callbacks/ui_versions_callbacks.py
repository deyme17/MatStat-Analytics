from typing import Callable
from dataclasses import dataclass

@dataclass
class DataVersionUICallbacks:
    set_version_list: Callable[[list[str]], None]
    set_current_index: Callable[[int], None]
    block_signals: Callable[[bool], None]

def build_data_version_callbacks(tab) -> DataVersionUICallbacks:
    return DataVersionUICallbacks(
        set_version_list=tab.data_version_combo.addItems,
        set_current_index=tab.data_version_combo.setCurrentIndex,
        block_signals=tab.data_version_combo.blockSignals
    )