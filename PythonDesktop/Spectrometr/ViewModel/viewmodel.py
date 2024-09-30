from PyQt5.QtCore import QObject, pyqtSignal
try:
    from Model.model import DataMode
except ImportError as e:
    print(f'Ошибка импорта: {e}')

class ViewModel(QObject):
    data_changed = pyqtSignal(list)
    disconnect_signal = pyqtSignal()
    connect_signal = pyqtSignal()
    new_data = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.model = DataMode()
        self.model.data_update.connect(self.on_data_received)
        self.time_update = None
        self.porog = None


    def fetch_data(self, value_sleep=1):
        self.model.read_data(value_sleep) # Запрос данных из модели

    def setting_new_values_configurate(self, porog, time):
        self.time_update = time
        self.porog = porog
        self.new_data.emit()
        self.model.install_new_config(porog, time)

    def on_data_received(seld,data):
        seld.data_changed.emit(data)

    def list_devices(self):
        return self.model.list_devices()
    def current_configuration(self):
        self.porog = self.model.get_cur_config()
        self.new_data.emit()
        return self.porog
    def current_time(self):
        self.time = self.time_update
        self.new_data.emit()
        return self.time
    
    def select_device(self, name_port, baud, time):
        self.model.select_device(name_port, baud, time)
        self.time_update = time
        self.new_data.emit()
        self.connect_signal.emit()

    def disconect_port(self):
        self.model.disconect_reading()
        self.disconnect_signal.emit()