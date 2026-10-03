from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor


TABLE_STYLE = """
QTableView {
    background-color: #ffffff;
    alternate-background-color: #f3f6fa;
    color: #131212;
    gridline-color: #d0d0d0;
    selection-background-color: #90caf9;
    selection-color: #131212;
}
QTableView::item:selected {
    background-color: #90caf9;
    color: #131212;
}
QHeaderView::section {
    background-color: #e3f2fd;
    color: #131212;
    border: 1px solid #bbdefb;
    padding: 3px;
}
"""


def apply_light_palette(app: QApplication) -> None:
    p = QPalette()
    p.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))
    p.setColor(QPalette.ColorRole.WindowText, QColor("#131212"))
    p.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
    p.setColor(QPalette.ColorRole.AlternateBase, QColor("#f3f6fa"))
    p.setColor(QPalette.ColorRole.Text, QColor("#131212"))
    p.setColor(QPalette.ColorRole.Button, QColor("#e8e8e8"))
    p.setColor(QPalette.ColorRole.ButtonText, QColor("#131212"))
    p.setColor(QPalette.ColorRole.ToolTipBase, QColor("#ffffdc"))
    p.setColor(QPalette.ColorRole.ToolTipText, QColor("#131212"))
    p.setColor(QPalette.ColorRole.Highlight, QColor("#90caf9"))
    p.setColor(QPalette.ColorRole.HighlightedText, QColor("#131212"))
    app.setPalette(p)
    


groupStyle = """
QGroupBox {
    border: 2px solid #87ceeb;
    border-radius: 10px;
    margin-top: 5px;
    background-color: rgba(135, 206, 235, 0.1);
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px;
}
"""
groupMargin = """QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            margin-top: -8px;
            left: 10px;
            padding: 0 5px;
            }
            """

appStyle = """
QWidget {
    background-color: rgb(240, 248, 255);
    color: black;
}

/* Загальні стилі для всіх основних елементів */
QPushButton, QCheckBox, QLabel, QSpinBox, QDoubleSpinBox, QComboBox, QTableWidget {
    background-color: rgb(240, 248, 255);
    color: black;
}

/* Стиль кнопок */
QPushButton {
    background-color: #5dade2;
    color: white;
    border-radius: 5px;
    padding: 5px;
}
QPushButton:hover {
    background-color: #2e86c1;
}
QPushButton:disabled {
    background-color: #bdc3c7;
    color: #666666;
}

/* Стиль для груп */
QGroupBox {
    background-color: rgb(240, 248, 255);
    color: black;
    border: 2px solid #87ceeb;
    border-radius: 10px;
}
QGroupBox:disabled {
    background-color: rgb(230, 230, 230);
    border: 2px dashed #aaa;
    color: gray;
}

/* Таблиця */
QTableWidget {
    background-color: rgb(255, 255, 255);
    color: black;
}
"""