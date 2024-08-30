import serial
import serial.tools.list_ports
from PyQt5.QtCore import pyqtSignal, QObject

class SerialPort(QObject):
    data_received = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.devices = [None]
        self.selected_port = None
        self.selected_baudrate = None

    def list_ports(self):
        ports = serial.tools.list_ports.comports()
        self.devices = []
        for port in ports:
            self.devices.append(port.device)

    def print_ports(self):
        for i,port in enumerate(self.devices):
            print(f"{i+1}. {port}")

    def input_selected_port(self, num_port):
        self.selected_port = num_port 
    
    def input_selected_baudrate(self, baud):
        self.selected_baudrate = int(baud)

    def read_uart(self):
        # with serial.Serial(self.selected_port, self.selected_baudrate, timeout=1) as ser:
            print(f"Подключено к {self.selected_port}. введенная скорость = {self.selected_baudrate} Начинаем чтение данных...")
            # while True:
                # line = ser.readline()
                # if line:
                    # data = line.decode('utf-8').strip()
            numbers = [10,4,100,20,41,1]#list(map(int, data.split('\r\n')))
            print("Полученные числа:", numbers)
            self.data_received.emit(numbers) # Отправляем данные на сигнал


def main():
    port = SerialPort()
    print("Доступные порты:")
    port.list_ports()
    port.print_ports()
    # port.input_selected_port()
    # port.input_selected_baudrate()
    # port.read_uart()

if __name__ == '__main__':
    main()
 