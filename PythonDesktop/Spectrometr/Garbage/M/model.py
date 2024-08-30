# Работа с USB
import usb.core
import usb.util
# Работа с UART
import serial
from M.serial_port import SerialPort
from PyQt5.QtCore import pyqtSignal, QObject

class DataModel(QObject):
    data_update = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.data = []
        self.device = None
        self.serial_port = SerialPort()
        self.serial_port.data_received.connect(self.on_data_received)

    def list_devices(self):
        self.serial_port.list_ports()
        self.serial_port.print_ports()
        return self.serial_port.devices

    def select_device(self, name_port, baud):
        print('TEST')
        self.serial_port.input_selected_port(name_port)
        self.serial_port.input_selected_baudrate(baud)
        self.serial_port.read_uart()

    def on_data_received(self, data):
        self.data_update.emit(data)
    def read_data(self):
        self.serial_port.read_uart()
    