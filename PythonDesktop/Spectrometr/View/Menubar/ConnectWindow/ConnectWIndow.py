from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow, QComboBox, QInputDialog, QMessageBox
from PyQt5.QtGui import QIcon

import numpy as np

connect_file_name_jpg = 'images/connect.jpg'

class ConnectWindow(QWidget):
    
    def __init__(self, viev_model):
        super().__init__()
        self.setWindowTitle('Connect Window')
        self.setWindowIcon(QIcon(connect_file_name_jpg))
        self.setGeometry(300,300,300,200)
        self.viev_model = viev_model
        self.initUI()
        self.baudrate = None
        self.device = None
        self.time = None
        self.time = None

    def initUI(self):

        layout = QVBoxLayout()

        self.label_baud = QLabel('Выберите частоту обновления (в секундах)')
        layout.addWidget(self.label_baud)
        self.list_time_update = QComboBox()
        self.set_list_time_upd()
        self.list_time_update.currentTextChanged.connect(self.selected_time)
        layout.addWidget(self.list_time_update)

        # Выбор устройства
        label_device = QLabel('Выберите устройство')
        layout.addWidget(label_device)
        self.device_selector = QComboBox()
        self.populate_devices()
        self.device_selector.currentTextChanged.connect(self.selected_devices)
        layout.addWidget(self.device_selector)

        ## Выбор скорости
        label_baud = QLabel('Выберите baudrate')
        layout.addWidget(label_baud)
        self.device_baudrate = QComboBox()
        self.list_baudrate()
        self.device_baudrate.currentTextChanged.connect(self.select_baudrete)
        self.device_baudrate.currentData()

        layout.addWidget(self.device_baudrate)

        self.button_connect = QPushButton('Подключиться')
        self.button_connect.clicked.connect(self.connect_device)
        layout.addWidget(self.button_connect)

        self.button_cancel = QPushButton('Отмена')
        self.button_cancel.clicked.connect(self.close)

        layout.addWidget(self.button_cancel)

        self.setLayout(layout)

    def populate_devices(self):
        devices = self.viev_model.list_devices()
        default_text = 'Выберите...'
        self.device_selector.addItem(default_text)
        if not devices:
            print('Нет доступных USB устройств')
            self.device_selector.addItem('Нет доступных USB устройств')
            return
        self.device_selector.addItems([f'{i}' for i in devices])

    def selected_devices(self):
        index = self.device_selector.currentIndex()
        if index != 0:
            device = self.device_selector.itemText(index)
            print(f'Выбранный device : {device}')
            self.device = device
        else:
            print('Выберите device')
            self.device = None
    def selected_time(self):
        index = self.list_time_update.currentIndex()
        if index != 0:
            self.time = self.list_time_update.itemText(index)
            print('selected time',self.time)
        else:
            self.time = None

    def populate_combobox(self, combobox, default_text, start, end, unit):
        combobox.addItem(default_text)
        if combobox == self.list_time_update:
            combobox.addItems([f'{i} {unit}' for i in range(5, 61, 5)])
        else:
            values = np.arange(start, end + 0.1, 0.1)
            combobox.addItems([f'{i:.1f}{unit}' for i in values])

    def set_list_time_upd(self):
        self.populate_combobox(self.list_time_update,'Выберите...', 5, 60, ' Сек')

    def select_baudrete(self):
        index = self.device_baudrate.currentIndex()
        print(f'index = {index}')
        if index != 0:
            baud = self.device_baudrate.itemText(index)
            print(f'Выбранный baudrate : {baud}')
            self.baudrate = baud
        else:
            print('Выберите баудрейт')
            self.baudrate = None

    def list_baudrate(self):
        default_text = 'Выберите...'
        self.device_baudrate.addItem(default_text)
        baud = ([9600,14400,19200,28800,38400, 56000, 57600, 115200, 128000,256000, 460800, 1000000])
        self.device_baudrate.addItems([str(i) for i in baud])

    def connect_device(self):
        if self.device and self.baudrate and self.time is not None:
            self.close()
            number = ''.join(filter(str.isdigit, self.time))
            selected = self.device, self.baudrate, number
            # text = "5 Сек"
            if selected:
                name_port, baud, time = selected
                try:
                    self.viev_model.select_device(name_port, baud, time)
                    print("Устройство выбрано:", selected)
                except ValueError as e:
                    print(e)
        else:
            self.show_dialog_error()
    def show_dialog_error(self):
        if not(self.baudrate and self.device_selector):
            QMessageBox.warning(self, 'Ошибка ввода', 'Пожалуйста, выберите все значения!')
        elif self.baudrate is None:
            QMessageBox.warning(self, 'Ошибка ввода', 'Пожалуйста, выберите Baudrate')
        elif self.device is None:
            QMessageBox.warning(self, 'Ошибка ввода', 'Пожалуйста, выберите device')
        elif self.list_time_update is None:
            QMessageBox.warning(self, 'Ошибка ввода', 'Пожалуйста, выберите время обновления')
            