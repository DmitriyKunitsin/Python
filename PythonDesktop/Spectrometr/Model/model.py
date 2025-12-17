from PyQt5.QtCore import QObject, pyqtSignal
import threading as th
try:
    from Model.serialport import SerialPort
except ImportError as e:
    print(f'Ошибка импорта: {e}')

class DataMode(QObject):

    data_update = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.serial_port = SerialPort()
        self.serial_port.data_received.connect(self.on_data_received)

    def read_data(self, value_sleep):
        print('Запрос на получение данных')
        #self.serial_port.start_reading(value_sleep) # Запуск чтения данных
        self.serial_port.start_simulating_reading(value_sleep)
    def list_devices(self):
        self.serial_port.list_ports()
        self.serial_port.print_ports()
        return self.serial_port.devices
    def get_cur_config(self):
        return self.serial_port.get_current_configuration()
    def install_new_config(self, porog, time):
        self.serial_port.new_configurate(porog, time)
    def on_data_received(self, data):
        self.data_update.emit(data)
    
    def select_device(self, name_port, baud, time):
        print('select_device')
        self.serial_port.input_selected_port(name_port)
        self.serial_port.input_selected_baudrate(baud)
        self.serial_port.serial_time = time
        th.Thread(daemon=True,target=self.serial_port.read_uart).start()

    def disconect_reading(self):
        self.serial_port.stop_reading()