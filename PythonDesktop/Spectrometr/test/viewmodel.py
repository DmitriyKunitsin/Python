from PyQt5.QtCore import QObject, pyqtSignal
from model import DataMode

class ViewModel(QObject):
    data_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.model = DataMode()
        self.model.data_update.connect(self.on_data_received)


    def fetch_data(self):
        self.model.read_data() # Запрос данных из модели

    def on_data_received(seld,data):
        seld.data_changed.emit(data)

    def list_devices(self):
        return self.model.list_devices()
    
    def select_device(self, name_port, baud):
        self.model.select_device(name_port, baud)