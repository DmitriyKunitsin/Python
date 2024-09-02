import time
import random
import threading
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
        self.running = None

    def start_reading(self, value_sleep):
        # Имитация асинхронного чтения данных
        # print('sleep = ', value_sleep)
        # time.sleep(float(value_sleep))
        numbers = np.random.randint(1, 1701, size=8191).tolist()
        self.data_received.emit(numbers) # Отправляем данные на сигнал
    
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
            # i = 0
            # self.start_thread_read_ueart()
        # with serial.Serial(self.selected_port, self.selected_baudrate, timeout=1) as ser:
            # while True:
            # while self.running.is_set():
                print(f"Подключено к {self.selected_port}. введенная скорость = {self.selected_baudrate} Начинаем чтение данных...")
                # if(i >= 2):
                #     self.running.clear()
                #     break
                # line = ser.readline()
                # if line:
                    # data = line.decode('utf-8').strip()
                numbers = np.random.randint(1, 1701, size=8191).tolist()#list(map(int, data.split('\r\n')))
                print("Полученны числа:")
                self.data_received.emit(numbers) # Отправляем данные на сигнал
                # time.sleep(2)
                # i+=1

    def start_thread_read_ueart(self):
        if self.running is not None and self.running.is_set():
            print('Чтение уже запущено')
            return
        self.running = threading.Event()# Инициализируем событие
        self.running.set() # Устанавливаем флаг для начала чтения  
        thread = threading.Thread(target=self.read_uart)
        # thread.daemon = True
        thread.start()
