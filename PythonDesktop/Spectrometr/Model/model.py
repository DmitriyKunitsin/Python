from PyQt5.QtCore import QObject, pyqtSignal
from Model.serialport import SerialPort

class DataMode(QObject):

    data_update = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.serial_port = SerialPort()
        self.serial_port.data_received.connect(self.on_data_received)

    def read_data(self):
        self.serial_port.start_reading() # Запуск чтения данных


    def on_data_received(self, data):
        self.data_update.emit(data)

    def list_devices(self):
        self.serial_port.list_ports()
        self.serial_port.print_ports()
        return self.serial_port.devices
    
    def select_device(self, name_port, baud):
        print('TEST')
        self.serial_port.input_selected_port(name_port)
        self.serial_port.input_selected_baudrate(baud)
        self.serial_port.read_uart()