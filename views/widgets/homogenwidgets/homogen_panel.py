from PyQt6.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QWidget
from abc import ABC, abstractmethod

from utils.ui_styles import groupStyle, groupMargin


class Meta(type(QGroupBox), type(ABC)):
    pass

class BaseHomoTestPanel(QGroupBox, ABC, metaclass=Meta):
    ...