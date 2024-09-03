from PyQt5.QtCore import QObject, pyqtSignal
try:
    from Model.model import DataMode
except ImportError as e:
    print(f'Ошибка импорта: {e}')

class ViewModel(QObject):
    data_changed = pyqtSignal(list)
    disconnect_signal = pyqtSignal()
    connect_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.model = DataMode()
        self.model.data_update.connect(self.on_data_received)


    def fetch_data(self, value_sleep=1):
        self.model.read_data(value_sleep) # Запрос данных из модели

    def on_data_received(seld,data):
        seld.data_changed.emit(data)

    def list_devices(self):
        return self.model.list_devices()
    
    def select_device(self, name_port, baud):
        self.model.select_device(name_port, baud)
        self.connect_signal.emit()

    def disconect_port(self):
        self.model.disconect_reading()
        self.disconnect_signal.emit()