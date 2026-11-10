from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QAbstractItemView
from .helpers import make_button

DEFAULT_LIST_HEIGHT = 110
DEFAULT_LIST_WIDTH = 310


class FeatureSelectorWidget(QGroupBox):
    """Reusable GUI subwidget for multi-selection feature/variable lists with action buttons."""
    def __init__(self, 
                 title: str = "Features (X)", 
                 label_prefix: str = "features", 
                 height: int = DEFAULT_LIST_HEIGHT, 
                 width: int = DEFAULT_LIST_WIDTH, 
                 parent=None):
        super().__init__(title, parent)
        self.label_prefix = label_prefix
        self.list_height = height
        self.list_width = width
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize child widgets and inner layouts."""
        layout = QVBoxLayout(self)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.list_widget.setMaximumHeight(self.list_height)
        self.list_widget.setMaximumWidth(self.list_width)

        btn_row = QHBoxLayout()
        self.select_all_btn = make_button("Select ALL", callback=self.select_all)
        self.clear_sel_btn = make_button("Clear selection", callback=self.clear_selection)
        btn_row.addWidget(self.select_all_btn)
        btn_row.addWidget(self.clear_sel_btn)

        self.count_label = QLabel(f"Selected: 0 {self.label_prefix}")

        layout.addWidget(self.list_widget)
        layout.addLayout(btn_row)
        layout.addWidget(self.count_label)

    def select_all(self) -> None:
        """Select all items present in the list widget."""
        self.list_widget.selectAll()

    def clear_selection(self) -> None:
        """Clear current item selection in the list widget."""
        self.list_widget.clearSelection()

    def get_selected_items(self) -> list[str]:
        """Return texts of currently selected items in list widget."""
        return [item.text() for item in self.list_widget.selectedItems()]

    def update_count_label(self) -> None:
        """Update count label with currently selected items count."""
        count = len(self.list_widget.selectedItems())
        self.count_label.setText(f"Selected: {count} {self.label_prefix}")

    def populate(self, items: list[str], select_all: bool = True) -> None:
        """Populate list widget with new items list."""
        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for item in items:
            self.list_widget.addItem(item)
        if select_all:
            self.list_widget.selectAll()
        self.list_widget.blockSignals(False)
        self.update_count_label()

    def set_enabled_state(self, enabled: bool) -> None:
        """Enable or disable subwidget user interaction components."""
        self.list_widget.setEnabled(enabled)
        self.select_all_btn.setEnabled(enabled)
        self.clear_sel_btn.setEnabled(enabled)