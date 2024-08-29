import sys
import usb.core
import usb.util
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import pyqtgraph as pg

# Model
class DataModel:
    def __init__(self):
        self.data = []
        self.device = None

    def list_devices(self):
        devices = []
        for dev in usb.core.find(find_all=True):
            devices.append({'idVendor':dev.idVendor,
                            'idProduct' :dev.idProduct,
                            'name' : usb.util.get_string(dev, dev.iProduct) if dev.iProduct else 'Неизвестный девайс'})
        return devices
    def select_device(self, idVendor, idProduct):
        self.device = usb.core.find(idVendor=idVendor, idProduct=idProduct)
        if self.device is None:
            raise ValueError('USB устройство не найдено')
        self.device.set_configuration()
    def read_data(self):
        if self.device is None:
            raise ValueError('USB устройство не выбрано')
        self.data = list(self.device.read(0x81, 64))  # Чтение данных (замените параметры на свои)
        return self.data
    
#VievModel
class ViewModel(QObject):
    data_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.model = DataModel()

    def fetch_data(self):
        data = self.model.read_data()
        self.data_changed.emit(data)

#View
class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.view_model = ViewModel()
        self.initUI()
        self.view_model.data_changed.connect(self.update_graph)

    def initUI(self):
        self.setWindowTitle("Spectrometr")
        layout = QVBoxLayout()

        self.device_selector = QComboBox()
        layout.addWidget(self.device_selector)

        self.button_selected_device = QPushButton('Выберите устройство')
        self.button_selected_device.clicked.connect(self.select_device) 
        layout.addWidget(self.button_selected_device)

        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        self.button_fetch_data  = QPushButton('Получить данные')
        self.button_fetch_data .clicked.connect(self.fetch_data)
        layout.addWidget(self.button_fetch_data )

        self.setLayout(layout)
    # Заполнение списка устройств
        self.populate_devices()

    def populate_devices(self):
        devices = self.view_model.model.list_devices()
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
                self.view_model.model.select_device(idVendor, idProduct)
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

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
