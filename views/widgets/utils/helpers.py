from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QFrame, QPushButton, QComboBox, QCheckBox, 
    QDoubleSpinBox, QWidget, QGroupBox
)
from PyQt6.QtCore import Qt


def create_section_header(text: str) -> QVBoxLayout:
    """Create styled section header layout with title label and horizontal separator line."""
    layout = QVBoxLayout()
    label = QLabel(text)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("""
        font-weight: 777;
        font-size: 12px;
        margin-top: 2px;
        margin-bottom: 1px;
    """)
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Sunken)
    layout.addWidget(label)
    layout.addWidget(line)
    return layout


def create_status_label() -> QLabel:
    """Create standardized status label with left alignment and fixed height."""
    label = QLabel()
    label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    label.setFixedHeight(30)
    label.setStyleSheet(
        "background:#ffffff; border:1px solid #ffffff; padding: 0 8px; border-radius:4px;"
    )
    return label


def update_status_label(label: QLabel, msg: str, ok: bool = True) -> None:
    """Update background color, border, and text of a status label based on ok flag."""
    color = "#e8f5e9" if ok else "#ffebee"
    border = "#a5d6a7" if ok else "#ef9a9a"
    label.setStyleSheet(
        f"background:{color}; border:1px solid {border}; padding: 0 8px; border-radius:4px;"
    )
    label.setText(msg)


def make_button(text: str, callback=None, enabled: bool = True, height: int | None = None, width: int | None = None) -> QPushButton:
    """Factory helper to build a styled QPushButton with optional fixed dimensions and callback."""
    btn = QPushButton(text)
    btn.setEnabled(enabled)
    if height is not None and width is not None:
        btn.setFixedSize(width, height)
    elif height is not None:
        btn.setFixedHeight(height)
    if callback:
        btn.clicked.connect(callback)
    return btn


def make_combo(on_change=None, enabled: bool = False) -> QComboBox:
    """Factory helper to build QComboBox with optional signal attachment."""
    combo = QComboBox()
    combo.setEnabled(enabled)
    if on_change:
        combo.currentIndexChanged.connect(on_change)
    return combo


def make_checkbox(text: str, checked: bool = False, callback=None) -> QCheckBox:
    """Factory helper to build QCheckBox with initial check state and callback."""
    cb = QCheckBox(text)
    cb.setChecked(checked)
    if callback:
        cb.toggled.connect(callback)
    return cb


def make_group_box(title: str, content: QWidget) -> QGroupBox:
    """Wrap a widget into a titled group box."""
    group = QGroupBox(title)
    layout = QVBoxLayout(group)
    layout.addWidget(content)
    return group


def make_alpha_spinbox(min_val: float = 0.01, max_val: float = 0.99, step: float = 0.01, decimals: int = 2, default: float = 0.05) -> QDoubleSpinBox:
    """Factory helper to build a configured QDoubleSpinBox for significance level alpha."""
    spinbox = QDoubleSpinBox()
    spinbox.setRange(min_val, max_val)
    spinbox.setSingleStep(step)
    spinbox.setDecimals(decimals)
    spinbox.setValue(default)
    return spinbox