from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow, QComboBox

class Setting_Command(QWidget):
    
    def __init__(self, viev_model):
        super().__init__()
        self.setWindowTitle('Setting Window')
        self.setGeometry(300,300,300,200)
        self.viev_model = viev_model
        self.initUI()
        self.value_sleep = 100

    def initUI(self):

        layout = QVBoxLayout()

        label_baud = QLabel('Выберите baudrate')
        layout.addWidget(label_baud)

        self.button_connect = QPushButton('Отправить')
        layout.addWidget(self.button_connect)

        self.setLayout(layout)

