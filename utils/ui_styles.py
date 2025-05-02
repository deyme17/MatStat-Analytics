groupStyle = """
QGroupBox {
    border: 2px solid #87ceeb;
    border-radius: 10px;
    margin-top: 10px;
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
QPushButton, QCheckBox, QLabel, QSpinBox, QDoubleSpinBox, QComboBox, QTableWidget {
    background-color: rgb(240, 248, 255);
    color: black;
}
QGroupBox {
    background-color: rgb(240, 248, 255);
    color: black;
    border: 2px solid #87ceeb;
    border-radius: 10px;
}
QTableWidget {
    background-color: rgb(255, 255, 255);
    color: black;
}
"""

buttonStyle = """
QPushButton {
    background-color: #3498db;
    color: white;
    border-radius: 5px;
    padding: 5px;
}
QPushButton:hover {
    background-color: #2980b9;
}
QPushButton:disabled {
    background-color: #bdc3c7;
}
"""
