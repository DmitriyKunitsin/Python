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
        self.time_update = 60000


    def fetch_data(self, value_sleep=1):
        self.model.read_data(value_sleep) # Запрос данных из модели

    def setting_new_values_configurate(self, porog):
        self.model.install_new_config(porog)

    def on_data_received(seld,data):
        seld.data_changed.emit(data)

    def list_devices(self):
        return self.model.list_devices()
    def current_configuration(self):
        return self.model.get_cur_config()
    
    def select_device(self, name_port, baud, time):
        self.model.select_device(name_port, baud, time)
        self.time_update = time
        self.connect_signal.emit()

    def disconect_port(self):
        self.model.disconect_reading()
        self.disconnect_signal.emit()