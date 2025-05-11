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