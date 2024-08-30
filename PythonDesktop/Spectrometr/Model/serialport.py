import time
import random
import serial
import serial.tools.list_ports
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal

class SerialPort(QObject):
    data_received = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.devices = [None]
        self.selected_port = None
        self.selected_baudrate = None

    def start_reading(self, value_sleep):
        # Имитация асинхронного чтения данных
        # time.sleep(1)  # Задержка для имитации чтения
        self.read_uart(value_sleep)
    
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

    def read_uart(self, value_sleep):
        # with serial.Serial(self.selected_port, self.selected_baudrate, timeout=1) as ser:
            print(f"Подключено к {self.selected_port}. введенная скорость = {self.selected_baudrate} Начинаем чтение данных...")
            # while True:
                # line = ser.readline()
                # if line:
                    # data = line.decode('utf-8').strip()
            # time.sleep(float(value_sleep))
            numbers = np.random.randint(1, 1701, size=255).tolist()#list(map(int, data.split('\r\n')))
            # print("Полученные числа:", numbers)
            self.data_received.emit(numbers) # Отправляем данные на сигнал
