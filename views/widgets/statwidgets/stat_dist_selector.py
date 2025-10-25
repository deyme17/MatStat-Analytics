from PyQt6.QtWidgets import QGroupBox, QGridLayout, QRadioButton, QButtonGroup
from typing import Callable, Optional
from utils.ui_styles import groupStyle, groupMargin
from models.stat_distributions import registered_distributions
from models.stat_distributions.stat_distribution import StatisticalDistribution

DIST_IN_ROW = 3
MAX_DIST_PANEL_HEIGHT = 100


class DistributionSelector(QGroupBox):
    """
    Widget for selecting statistical distributions.
    Provides radio buttons for all registered distributions.
    """
    def __init__(self, parent=None):
        """
        Initialize the distribution selector.
        Args:
            parent: Optional QWidget parent.
        """
        super().__init__("Statistical Distributions", parent)
        self._on_change: Optional[Callable[[], None]] = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Initialize UI components."""
        self.setMaximumHeight(MAX_DIST_PANEL_HEIGHT)
        self.setStyleSheet(groupStyle + groupMargin)

        self.button_group = QButtonGroup(self)
        layout = QGridLayout()

        self._add_none_option(layout)
        self._add_distribution_options(layout)

        self.setLayout(layout)

    def _add_none_option(self, layout: QGridLayout) -> None:
        """Add 'None' option to selector."""
        self.none_btn = QRadioButton("None")
        self.button_group.addButton(self.none_btn)
        layout.addWidget(self.none_btn, 0, 0)
        self.none_btn.toggled.connect(self._handle_change)
        self.none_btn.setChecked(True)

    def _add_distribution_options(self, layout: QGridLayout) -> None:
        """Add registered distributions as options."""
        for index, (name, _) in enumerate(registered_distributions.items()):
            btn = QRadioButton(name)
            self.button_group.addButton(btn)
            layout.addWidget(btn, (index + 1) // DIST_IN_ROW, (index + 1) % DIST_IN_ROW)
            btn.toggled.connect(self._handle_change)

    def get_selected_distribution(self) -> Optional[StatisticalDistribution]:
        """
        Get an instance of the currently selected distribution.
        Returns:
            StatisticalDistribution or None
        """
        btn = self.button_group.checkedButton()
        if btn and btn.text() != "None":
            return registered_distributions[btn.text()]()
        return None

    def reset_selection(self) -> None:
        """Reset selection to 'None'."""
        self.none_btn.setChecked(True)

    def _handle_change(self) -> None:
        """Internal handler for button state change."""
        if self._on_change:
            self._on_change()

    def set_on_change(self, callback: Callable[[], None]) -> None:
        """
        Set callback for distribution selection changes.
        Args:
            callback: A function to call on change.
        """
        self._on_change = callback