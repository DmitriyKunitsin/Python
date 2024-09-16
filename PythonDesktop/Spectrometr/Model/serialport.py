import time
import random
import struct
import threading
import serial
import serial.tools.list_ports
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal


from Model.SKLP import SKLP_Serial, SKLP_GGLP_Spectr

class SerialPort(QObject):
    data_received = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.devices = [None]
        self.selected_port = None
        self.selected_baudrate = None
        self.running = False
        self.SKLP = None
        self.serial_time = None
    def start_reading(self, value_sleep):
        ''' Запускает команду на чтения данных с микроконтроллера

        :param value_sleep: TODO типо передавать сюдда значение ожидания, но не актуально уже
        
        :return: Возвращает накопленные данные микроконтроллером 
        '''
        # if self.port and self.baud is not None:
        # port = SKLP_Serial(Baud=self.selected_baudrate,Port=self.selected_port)
        # sklp = SKLP_GGLP_Spectr(Address=SKLP_GGLP_Spectr.Spectr_Address.GET_YOUR_SEARIAL_NUMBER, Interface=port)
        if self.SKLP is not None:
            try:
                check_connec = self.SKLP.Query_GetID()
                if check_connec:
                    answer_packet =  self.SKLP.Query(self.SKLP.Enum_Command.GET_ALL_DATA_SPECTR)
                    numbers = self.parse_data(answer_packet)
                    self.data_received.emit(list(numbers)) # Отправляем данные на сигнал
                else:
                    raise ValueError('Не удалось найти нужный микроконтроллер, убедитесь, что он подключен')
            except ValueError as e:
                print(e)
        else:
            print('не подключен к устройству')
            error = [f'Error : Устройство не подключено']
            self.data_received.emit(error) 
    
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

    # def frecyh_data(self, time, porog, ):
    def max_value(self,data):
        temp = data[0]
        for i in data:
            if temp < i:
                temp = i 
        return temp
    def parse_data(self,data):
        parsed_values = []
        
        # (2 байта для uint16)
        size_of_int = 2
        
        # Обход данных с шагом по размеру целого числа
        for i in range(0, len(data), size_of_int):
            if i + 2 < len(data):
                # Извлечение подстроки и распаковка
                chunk = data[i:i + size_of_int]
                if len(chunk) == size_of_int:
                    value = struct.unpack('<H', chunk)[0]  # '>H' - big-endian uint16
                    parsed_values.append(value)
        
        return parsed_values
    def parse_data_byte(self,data):
        data_list = []
        numbers = [int.from_bytes(data[j:j+2], byteorder='big') for j in range(0, len(data), 2)]
        for i in numbers:
            data_list.append(i)
        return data_list
    def read_uart(self):
        self.running = True
        print(f"Подключено к {self.selected_port}. Введенная скорость = {self.selected_baudrate}. Начинаем чтение данных...")
        try:
            self.PORT = SKLP_Serial(Port=self.selected_port, Baud=self.selected_baudrate)
            self.SKLP = SKLP_GGLP_Spectr(Address=SKLP_GGLP_Spectr.Spectr_Address.GET_YOUR_SEARIAL_NUMBER, Interface=self.PORT)
    
            try:
                while self.running:
                    print('Проверка подключения')
                    check_connect = self.SKLP.Query_GetID()
                    if check_connect:
                        print(f'Ждем ... {self.serial_time} сек')
                        self.start_reading(1)
                        time.sleep(float(self.serial_time))
                    else:
                        raise ValueError('Устройство не подключено!!')
                
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
        except:
            self.serial_time = self.serial_time
        
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
