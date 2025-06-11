from PyQt6.QtWidgets import QGroupBox, QGridLayout, QRadioButton, QButtonGroup
from utils.ui_styles import groupStyle, groupMargin
from models.stat_distributions import registered_distributions
from models.stat_distributions.stat_distribution import StatisticalDistribution

class DistributionSelector(QGroupBox):
    """Widget for selecting statistical distributions."""
    def __init__(self, on_change=None, parent=None):
        super().__init__("Statistical Distributions", parent)
        self._on_change = on_change
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI components."""
        self.setMaximumHeight(100)
        self.setStyleSheet(groupStyle + groupMargin)
        
        self.button_group = QButtonGroup(self)
        layout = QGridLayout()
        
        self._add_none_option(layout)
        self._add_distribution_options(layout)
        
        self.setLayout(layout)

    def _add_none_option(self, layout):
        """Add 'None' option to selector."""
        self.none_btn = QRadioButton("None")
        self.button_group.addButton(self.none_btn)
        layout.addWidget(self.none_btn, 0, 0)
        self.none_btn.toggled.connect(self._handle_change)
        self.none_btn.setChecked(True)

    def _add_distribution_options(self, layout):
        """Add registered distributions as options."""
        for index, (name, _) in enumerate(registered_distributions.items()):
            btn = QRadioButton(name)
            self.button_group.addButton(btn)
            layout.addWidget(btn, (index + 1) // 3, (index + 1) % 3)
            btn.toggled.connect(self._handle_change)

    def get_selected_distribution(self) -> StatisticalDistribution | None:
        """Get currently selected distribution instance."""
        btn = self.button_group.checkedButton()
        if btn and btn.text() != "None":
            return registered_distributions[btn.text()]()
        return None

    def reset_selection(self):
        """Reset selection to 'None'."""
        self.none_btn.setChecked(True)

    def _handle_change(self):
        """Handle distribution selection change."""
        if self._on_change:
            self._on_change()

    def set_on_change(self, callback):
        """Set callback for distribution changes."""
        self._on_change = callback