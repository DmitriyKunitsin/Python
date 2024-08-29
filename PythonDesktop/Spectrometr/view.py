from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox
import pyqtgraph as pg

class MainWindow(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.initUI()
        self.view_model.data_changed.connect(self.update_graph)
        self.populate_devices()

    def initUI(self):
        self.setWindowTitle("Spectromетр")
        layout = QVBoxLayout()

        self.device_selector = QComboBox()
        layout.addWidget(self.device_selector)

        self.button_selected_device = QPushButton('Выберите устройство')
        self.button_selected_device.clicked.connect(self.select_device)
        layout.addWidget(self.button_selected_device)

        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        self.button_fetch_data = QPushButton('Получить данные')
        self.button_fetch_data.clicked.connect(self.fetch_data)
        layout.addWidget(self.button_fetch_data)

        self.setLayout(layout)

    def populate_devices(self):
        devices = self.view_model.list_devices()
        if not devices:
            print('Нет доступных USB устройств')
            return
        for device in devices:
            self.device_selector.addItem(f"{device['name']} (Vendor: {device['idVendor']:04x}, Product: {device['idProduct']:04x})",
                                          (device['idVendor'], device['idProduct']))

    def select_device(self):
        selected = self.device_selector.currentData()
        if selected:
            idVendor, idProduct = selected
            try:
                self.view_model.select_device(idVendor, idProduct)
                print("Устройство выбрано:", selected)
            except ValueError as e:
                print(e)

    def fetch_data(self):
        try:
            self.view_model.fetch_data()
        except ValueError as e:
            print(e)

    def update_graph(self, data):
        self.plot_widget.clear()
        self.plot_widget.plot(data, pen='g')
