from typing import Callable
from dataclasses import dataclass

@dataclass
class ComboUICallbacks:
    set: Callable[[list[str]], None]
    set_current_index: Callable[[int], None]
    block_signals: Callable[[bool], None]

def build_combo_callbacks(combo) -> ComboUICallbacks:
    def set_list(items: list[str]) -> None:
        """Clear combo and set new items list"""
        combo.clear()
        combo.addItems(items)
    
    return ComboUICallbacks(
        set=set_list,
        set_current_index=combo.setCurrentIndex,
        block_signals=combo.blockSignals
    )