from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow, QComboBox
from View.ConnectWindow.device_selector import DeviceSelector


class ConnectWindow(QWidget):
    
    def __init__(self, viev_model):
        super().__init__()
        self.setWindowTitle('Connect Window')
        self.setGeometry(300,300,300,200)
        self.viev_model = viev_model
        self.initUI()
        self.populate_devices()
        self.baudrate = 0
        # central_widget = QWidget()
        # self.setCentralWidget(central_widget)

    def initUI(self):

        layout = QVBoxLayout()
        # Выбор устройства
        label_device = QLabel('Выберите устройство')
        layout.addWidget(label_device)
        self.device_selector = DeviceSelector(self.viev_model)
        self.device_selector.device_selected.connect(self.on_device_selected)
        layout.addWidget(self.device_selector)



        ## Выбор скорости
        label_baud = QLabel('Выберите baudrate')
        layout.addWidget(label_baud)
        self.device_baudrate = QComboBox()
        self.list_baudrate()
        self.device_baudrate.currentIndexChanged.connect(self.select_baudrete)
        self.device_baudrate.currentData()

        layout.addWidget(self.device_baudrate)

        self.button_connect = QPushButton('Подключиться')
        self.button_connect.clicked.connect(self.select_device)
        layout.addWidget(self.button_connect)



        self.setLayout(layout)

    def select_baudrete(self):
        index = self.device_baudrate.currentIndex()
        baud = self.device_baudrate.itemText(index)
        print(f'Выбранный baudrate : {baud}')
        self.baudrate = baud
    def list_baudrate(self):
        baud = [0,14400,19200,28800,38400, 56000, 57600, 115200, 128000,256000, 460800]
        for i in baud:
            self.device_baudrate.addItem(str(i))

    def select_device(self):
        selected = self.device_selector.get_selected_device(), self.baudrate
        if selected:
            name_port, baud = selected
            try:
                self.viev_model.select_device(name_port, baud)
                # self.view_model.select_device(idVendor, idProduct)
                print("Устройство выбрано:", selected)
                
            except ValueError as e:
                print(e)
    def on_device_selected(self, selected_device):
        if selected_device is not None:
            self.selected_device = selected_device
            print("Устройство выбрано:", selected_device)

    def populate_devices(self):
        devices = self.viev_model.list_devices()
        if not devices:
            print('Нет доступных USB устройств')
            self.device_selector.addItem('Нет доступных USB устройств')
            return
        self.device_selector.add_item(devices)