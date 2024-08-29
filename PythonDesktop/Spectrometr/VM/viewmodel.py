from PyQt5.QtCore import pyqtSignal, QObject
from M.model import DataModel

class ViewModel(QObject):
    data_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.model = DataModel()

    def fetch_data(self):
        data = self.model.read_data()
        self.data_changed.emit(data)

    def list_devices(self):
        return self.model.list_devices()

    def select_device(self, idVendor, idProduct):
        self.model.select_device(idVendor, idProduct)
