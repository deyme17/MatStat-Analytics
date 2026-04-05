from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QListWidgetItem, QAbstractItemView
)
import pandas as pd


class StandardizeDialog(QDialog):
    """
    Dialog for selecting columns to normalize/unnormalize.
    """
    def __init__(self, dataframe: pd.DataFrame, std_params: dict | None = None, parent=None):
        """
        Args:
            dataframe: current DataFrame to pick columns from
            std_params: existing params for current dataset — if set, shows hint and enables Unnormalize
            parent: parent widget
        """
        super().__init__(parent)
        self.setWindowTitle("Standardize Columns")
        self.setMinimumWidth(320)

        self._df = dataframe
        self._std_params = std_params
        self._result_columns: list[str] | None = None
        self._action: str | None = None  # 'normalize' | 'unnormalize'

        self._init_ui()

    @property
    def selected_columns(self) -> list[str] | None:
        return self._result_columns

    @property
    def action(self) -> str | None:
        return self._action

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Select columns to standardize:"))

        self._list = QListWidget()
        self._list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self._populate_list()
        self._list.selectAll()
        layout.addWidget(self._list)

        if self._std_params:
            cols = ", ".join(self._std_params.keys()) if 'mean' not in self._std_params else "current column"
            hint = QLabel(f"Currently normalized: {cols}")
            hint.setStyleSheet("color: gray; font-size: 11px;")
            layout.addWidget(hint)

        btn_layout = QHBoxLayout()

        self._normalize_btn = QPushButton("Normalize")
        self._normalize_btn.clicked.connect(self._on_normalize)
        btn_layout.addWidget(self._normalize_btn)

        self._unnormalize_btn = QPushButton("Unnormalize")
        self._unnormalize_btn.setEnabled(self._std_params is not None)
        self._unnormalize_btn.clicked.connect(self._on_unnormalize)
        btn_layout.addWidget(self._unnormalize_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

    def _populate_list(self) -> None:
        """Fill list with all numeric columns, no filtering."""
        for col in self._df.select_dtypes(include='number').columns:
            self._list.addItem(QListWidgetItem(col))

    def _on_normalize(self) -> None:
        cols = [item.text() for item in self._list.selectedItems()]
        if not cols:
            return
        self._result_columns = cols
        self._action = 'normalize'
        self.accept()

    def _on_unnormalize(self) -> None:
        self._action = 'unnormalize'
        self.accept()