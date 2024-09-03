from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow, QComboBox, QInputDialog, QMessageBox
from PyQt5.QtGui import QIcon

connect_file_name_jpg = 'images/connect.jpg'

class ConnectWindow(QWidget):
    
    def __init__(self, viev_model, menu_bar):
        super().__init__()
        self.setWindowTitle('Connect Window')
        self.setWindowIcon(QIcon(connect_file_name_jpg))
        self.setGeometry(300,300,300,200)
        self.menu_bar = menu_bar
        self.viev_model = viev_model
        self.initUI()
        self.baudrate = None
        self.device = None

    def initUI(self):

        layout = QVBoxLayout()
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
        baud = ([9600,14400,19200,28800,38400, 56000, 57600, 115200, 128000,256000, 460800])
        self.device_baudrate.addItems([str(i) for i in baud])

    def connect_device(self):
        if self.device and self.baudrate is not None:
            self.close()
            selected = self.device, self.baudrate
            if selected:
                name_port, baud = selected
                try:
                    self.viev_model.select_device(name_port, baud)
                    self.menu_bar.update_status(True)
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
            