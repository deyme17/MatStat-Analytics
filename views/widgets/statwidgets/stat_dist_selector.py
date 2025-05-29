from PyQt6.QtWidgets import QGroupBox, QGridLayout, QRadioButton, QButtonGroup
from utils.ui_styles import groupStyle, groupMargin
from models.stat_distributions import registered_distributions

class DistributionSelector(QGroupBox):
    def __init__(self, on_change=None, parent=None):
        super().__init__("Statistical Distributions", parent)
        self.setMaximumHeight(100)
        self.setStyleSheet(groupStyle + groupMargin)

        self.button_group = QButtonGroup(self)
        layout = QGridLayout()

        # Add "None" option
        self.none_btn = QRadioButton("None")
        self.button_group.addButton(self.none_btn)
        layout.addWidget(self.none_btn, 0, 0)
        if on_change:
            self.none_btn.toggled.connect(on_change)
        self.none_btn.setChecked(True)

        for index, (name, dist_cls) in enumerate(registered_distributions.items()):
            btn = QRadioButton(name)
            self.button_group.addButton(btn)
            layout.addWidget(btn, (index + 1) // 3, (index + 1) % 3)
            if on_change:
                btn.toggled.connect(on_change)

        self.setLayout(layout)

    def get_selected_distribution(self):
        btn = self.button_group.checkedButton()
        if btn and btn.text() != "None":
            return registered_distributions[btn.text()]()
        return None

    def reset_selection(self):
        self.none_btn.setChecked(True)
