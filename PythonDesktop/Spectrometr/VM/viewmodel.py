from PyQt5.QtCore import pyqtSignal, QObject
from M.model import DataModel

class ViewModel(QObject):
    data_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.model = DataModel()
        self.model.data_update.connect(self.on_data_received)

    def fetch_data(self):
        try:
            data = self.model.read_data()
            # print(data)
            if data is None:
                raise ValueError('Данные не были получены (None)')
            self.data_changed.emit(data)
        except ValueError as e:
            print(e)

    def list_devices(self):
        return self.model.list_devices()

    def select_device(self, name_port, baud):
        self.model.select_device(name_port, baud)

    def on_data_received(self, data):
        self.data_changed.emit(data)
