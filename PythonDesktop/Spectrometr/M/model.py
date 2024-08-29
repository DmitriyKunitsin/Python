# Работа с USB
import usb.core
import usb.util
# Работа с UART
import serial
from M.serial_port import SerialPort

class DataModel:
    def __init__(self):
        self.data = []
        self.device = None

    def list_devices(self):
        dev = SerialPort()
        dev.list_ports()
        dev.print_ports()
        return dev.devices

        # devices = []
        # for dev in usb.core.find(find_all=True):
        #     devices.append({'idVendor': dev.idVendor,
        #                     'idProduct': dev.idProduct,
        #                     'name': usb.util.get_string(dev, dev.iProduct) if dev.iProduct else 'Неизвестный девайс'})
        # return devices

    def select_device(self, idVendor, idProduct):
        self.device = usb.core.find(idVendor=idVendor, idProduct=idProduct)
        if self.device is None:
            raise ValueError('USB устройство не найдено')
        self.device.set_configuration()

    def read_data(self):
        if self.device is None:
            raise ValueError('USB устройство не выбрано')
        self.data = list(self.device.read(0x81, 64))  
        return self.data
    
    def read_data(self):
        uart = serial.Serial()
