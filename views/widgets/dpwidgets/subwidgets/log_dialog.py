from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QCheckBox, QButtonGroup, QFrame
)

LOG_KINDS = [
    ("ln",   "ln - natural logarithm  (base e)"),
    ("lg",   "lg - decimal logarithm   (base 10)"),
    ("log2", "log₂ - binary logarithm   (base 2)"),
]


class LogTransformDialog(QDialog):
    """
    Dialog for choosing a logarithmic transform type and
    whether to apply the forward or inverse transform.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Log Transform")
        self.setMinimumWidth(340)

        self._kind: str | None = None
        self._inverse: bool = False

        self._init_ui()

    @property
    def kind(self) -> str | None:
        return self._kind

    @property
    def inverse(self) -> bool:
        return self._inverse

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        header = QLabel("Logarithm Kind:")
        header.setStyleSheet("font-weight: bold;")
        layout.addWidget(header)

        self._btn_group = QButtonGroup(self)
        self._radio_buttons: dict[str, QRadioButton] = {}

        radio_frame = QFrame()
        radio_layout = QVBoxLayout(radio_frame)
        radio_layout.setContentsMargins(8, 4, 8, 4)
        radio_layout.setSpacing(6)

        for i, (kind, label) in enumerate(LOG_KINDS):
            rb = QRadioButton(label)
            if i == 0:
                rb.setChecked(True) # default: ln
            self._btn_group.addButton(rb)
            self._radio_buttons[kind] = rb
            radio_layout.addWidget(rb)

        layout.addWidget(radio_frame)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(sep)

        self._inverse_check = QCheckBox("Inverse transformation")
        layout.addWidget(self._inverse_check)

        # buttons
        btn_layout = QHBoxLayout()

        apply_btn = QPushButton("Apply")
        apply_btn.setDefault(True)
        apply_btn.clicked.connect(self._on_apply)
        btn_layout.addWidget(apply_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

    def _on_apply(self) -> None:
        for kind, rb in self._radio_buttons.items():
            if rb.isChecked():
                self._kind = kind
                break
        self._inverse = self._inverse_check.isChecked()
        self.accept()