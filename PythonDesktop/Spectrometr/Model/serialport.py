import time
import random
import struct
import threading
import serial
import serial.tools.list_ports
import numpy as np
from struct import *
import struct
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
        '''Заполняет список всеми доступными USB устройствами
        
        
        :return: Список доступных USB устройств'''
        ports = serial.tools.list_ports.comports()
        self.devices = []
        for port in ports:
            self.devices.append(port.device)
    def get_current_configuration(self):
        '''Делает запрос на текущие установленные конфигурационные данные
        
        :return: отформатированное значение установленных конфигураций'''
        config = self.SKLP.Query(self.SKLP.Enum_Command.GET_CONFIGURATION)
        number = struct.unpack('f', config[:4])[0]  # Извлекаем первые 4 байта и преобразуем в float
        print('Текущие конфигурации',f'{number:.1f}')
        formated_number = f'{number:.1f}'
        return formated_number
    def new_configurate(self, porog):
        '''Устанавливает новые конфигурации в плате
        
        :param porog: Пороговое значение для считывания спектра
        
        
        :raise: В случае не успешной установки значений, возвращает ошибку, которая вызывает окно предуупреждение'''
        try:
            filtered_string = '.'.join(filter(str.isdigit, porog))
            new_config = self.SKLP.Query(self.SKLP.Enum_Command.SET_CONFIGURATION, pack('f', float(filtered_string)))
            if not new_config:
                print('Не удалось установить параметры')
            else:
                try:
                    number = struct.unpack('f', new_config[:4])[0]
                    print('Успешно установил конфиг : ',f'{number:.1f} Вольта')
                except:
                    print('не удалось преобразовать')
        except:
            error = [f'Error : Неудалось установить значения конфигурации']
            self.data_received.emit(error) 
    def print_ports(self):
        for i,port in enumerate(self.devices):
            print(f"{i+1}. {port}")

    def input_selected_port(self, num_port):
        self.selected_port = num_port 
    
    def input_selected_baudrate(self, baud):
        self.selected_baudrate = int(baud)

    def max_value(self,data):
        temp = data[0]
        for i in data:
            if temp < i:
                temp = i 
        return temp
    def parse_data(self,data):
            '''
                Парсит входные данные и извлекает значения типа uint16.

                Эта функция принимает байтовые данные и извлекает из них 16-битные целые числа
                без знака (uint16), используя порядок байтов little-endian. Каждый uint16 занимает
                2 байта, и функция обрабатывает данные с шагом в 2 байта.

                Параметры:
                ----------
                :param data: bytes
                    Входные данные в виде байтовой строки, содержащие значения типа uint16.

                Возвращает:
                ----------
                list
                    Список извлеченных значений типа uint16.

                Исключения:
                -----------
                ValueError:
                    Может быть вызвано, если данные не могут быть распакованы в формате uint16.

                Примечания:
                ----------
                Функция игнорирует оставшиеся байты, если длина данных не кратна 2.
                Например, если длина данных равна 5, то будет обработано только первые 4 байта.
                
                Пример использования:
                --------------------
                data = b'\\x01\\x02\\x03\\x04\\x05'
                parsed_values = self.parse_data(data)
                # parsed_values будет равен [512, 1024]
            '''
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
    def read_uart(self):
            """
                Устанавливает соединение с UART и начинает чтение данных.

                Эта функция инициирует подключение к выбранному последовательному порту с заданной
                скоростью передачи данных (baudrate). После успешного подключения функция проверяет
                наличие устройства и начинает процесс чтения данных. Если устройство не подключено,
                будет вызвано исключение.

                Параметры:
                ----------
                Нет.

                Возвращает:
                ----------
                Нет.

                Исключения:
                -----------
                serial.SerialException:
                    Вызывается, если происходит ошибка подключения к последовательному порту.
                
                PermissionError:
                    Вызывается, если отсутствует доступ к порту.
                
                Exception:
                    Любая другая непредвиденная ошибка во время выполнения.

                Примечания:
                ----------
                - Функция использует объект SKLP_Serial для управления последовательным портом
                и объект SKLP_GGLP_Spectr для взаимодействия с устройством.
                - В случае успешного подключения функция вызывает метод get_current_configuration
                и начинает чтение данных с помощью метода start_reading.
                - В случае ошибки подключения или доступа, сообщение об ошибке будет отправлено
                через сигнал data_received.

                Пример использования:
                --------------------
                # Предполагается, что экземпляр класса уже инициализирован и настроен.
                self.read_uart()
            """
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
                            self.get_current_configuration()
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
        """
        Меняет значение переменной эземпляра класса self.running, устанавливания значение false
        """
        self.running = False
        print('Отключен от порта')

    def start_thread_read_ueart(self):
            """
            Запускает поток для чтения данных из UART.

            Эта функция инициализирует новый поток, который будет выполнять метод read_uart.
            Если чтение уже запущено, функция выводит сообщение и не запускает новый поток.

            Параметры:
            ----------
            Нет.

            Возвращает:
            ----------
            Нет.

            Исключения:
            -----------
            Нет. 

            Примечания:
            ----------
            - Функция использует объект threading.Event для управления состоянием чтения.
            - Если чтение уже запущено (флаг running установлен), новая попытка запуска
            будет проигнорирована, и в консоль будет выведено сообщение.
            - Новый поток создается с помощью threading.Thread, который выполняет метод
            read_uart. 

            Пример использования:
            --------------------
            # Предполагается, что экземпляр класса уже инициализирован и настроен.
            self.start_thread_read_uart()
            """
            if self.running is not None and self.running.is_set():
                print('Чтение уже запущено')
                return
            self.running = threading.Event()# Инициализируем событие
            self.running.set() # Устанавливаем флаг для начала чтения  
            thread = threading.Thread(target=self.read_uart)
            # thread.daemon = True
            thread.start()
