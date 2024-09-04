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
        self.running = False

    def start_reading(self, value_sleep):
        # Имитация асинхронного чтения данных
        print('sleep = ', value_sleep)
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
        self.running = True
        print(f"Подключено к {self.selected_port}. Введенная скорость = {self.selected_baudrate}. Начинаем чтение данных...")
        try:
            with serial.Serial(self.selected_port, self.selected_baudrate, timeout=1, bytesize=8, parity='N', stopbits=1) as ser:
                data_list = []
                i = 0
                last_received_time = time.time()
                timeout_duration = 2 # Время ожидания окончания пакета в секундах
                while self.running:
                    if ser.in_waiting > 0:
                        line = ser.readline()  # Читаем строку
                        if line:
                            decoded_line = line.decode('utf-8', errors='ignore').strip()
                            
                            if decoded_line.isdigit():
                                last_received_time = time.time() 
                                data_list.append(int(decoded_line))
                    # Проверяем таймаут
                    if time.time() - last_received_time > timeout_duration and data_list:
                        print(f"Получен пакет № {i+1}: {data_list}")
                        self.data_received.emit(data_list)
                        i+=1
                        data_list.clear() # очистка списка
        except serial.SerialException as e:
            print(f'Ошибка подключения к порту: {e}')
            error = [f'Error : {e}']
            self.data_received.emit(error)
        except PermissionError as e:
            error = [f'Error : {e}']
            self.data_received.emit(error) 
            print(f'Ошибка доступа к порту: {e}')
        except Exception as e:
            error = [f'Error : {e}']
            self.data_received.emit(error) 
            print(f'Произошла непредвиденная ошибка: {e}')
            print('Error ',e)
        
    def stop_reading(self):
        self.running = False
        print('Отключен от порта')

    def start_thread_read_ueart(self):
        if self.running is not None and self.running.is_set():
            print('Чтение уже запущено')
            return
        self.running = threading.Event()# Инициализируем событие
        self.running.set() # Устанавливаем флаг для начала чтения  
        thread = threading.Thread(target=self.read_uart)
        # thread.daemon = True
        thread.start()
