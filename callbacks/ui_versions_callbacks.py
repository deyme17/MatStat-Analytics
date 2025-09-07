from typing import Callable
from dataclasses import dataclass

@dataclass
class DataVersionUICallbacks:
    set_version_list: Callable[[list[str]], None]
    set_current_index: Callable[[int], None]
    block_signals: Callable[[bool], None]

def build_data_version_callbacks(data_version_combo) -> DataVersionUICallbacks:
    def set_version_list(items: list[str]) -> None:
        """Clear combo and set new items list"""
        data_version_combo.clear()
        data_version_combo.addItems(items)
    
    return DataVersionUICallbacks(
        set_version_list=set_version_list,
        set_current_index=data_version_combo.setCurrentIndex,
        block_signals=data_version_combo.blockSignals
    )