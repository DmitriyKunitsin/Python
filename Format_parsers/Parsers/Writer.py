import os
import json
import datetime
from typing import Optional
import struct
from itertools import islice


valid_split_format = {0x20, 0x10, 0x40, 0x51, 0x33}
valid_split_deviceId = {0x32, 0x33, 0x34, 0x35}
class FileSplitWriter:
    """Потоковый писатель, разбивающий вывод на файлы по достижению лимита байт исходного файла."""
    def __init__(self, base_dir: str, base_name: str, bytes_per_file: int, ext: str = "csv"):
        self.base_dir = base_dir
        self.base_name = base_name
        self.bytes_per_file = bytes_per_file
        self.ext = ext
        self._current_file = None
        self._part_number = 1
        self._next_threshold = bytes_per_file
        self._count_record = 0        

    def _open_new_file(self):
        if self._current_file:
            self._current_file.close()
        filename = f"{self.base_name}.part{self._part_number}.{self.ext}"
        path = os.path.join(self.base_dir, filename)
        self._current_file = open(path, 'w', encoding='utf-8')
        self._current_file.write("timestamp,payload_length\n")
        self._part_number += 1
        print(f"Создан новый файл: {path}")
    def packet_parse_0x10(self, data):
        """
        Парсер пакета ДОЛ
        Структура :
        int32 - квадратурный энкодер
        """
        pars_data = struct.unpack(f'=i', data)
        line = " DOL : " + json.dumps(
            {
                "encoder" : pars_data
            }
        )
        return line
    def packet_parse_0x20(self, data):
        """
        Парсер пакет Датчика натяжения каната
        Структура :
        float - натяжение [кг/с]
        """
        pars_data = struct.unpack(f'=f',data)
        line = " DNTK : " + json.dumps(
            {
                "tension": pars_data
            }
        )
        return line
    def packet_parse_0x33(self, data):
        """
        Парсер пакета датчика давления
        
        Структура (8 байт):
        uint8_t - предыдущий токен
        uint16_t - счетчик данных, накопленных по предыдущему токену
        float - давление [PUnits] (бар)
        uint16_t - давление [ADC16] (ADC24/256)
        """
        pars_data = struct.unpack(f'=BHfH', data[:9])
        prev_token, cnt_data, press_bar, press_adc = pars_data
        packet_data = data[9:]
        line = " 2DD : "+json.dumps({
            "prev_token": prev_token,
            "cnt_data": cnt_data,
            "press_bar": press_bar,
            "press_adc": press_adc,
            "Data": list(packet_data)
        })
        return line
    def packet_parse_0x40(self, data):
        """
        Парсер пакета синхронизации
        Структура :
        uint8 - Токен
        uint8 - Dummy
        time_t - Time
        uint16 - SubSecond 
        """
        pars_data = struct.unpack(f'=BBLH',data)
        token,dummy,time,SubSecond = pars_data
        print('='*80)
        print('Команда 0х40 :')
        print(f' token : {token}')
        print(f' dummy : {dummy}')
        print(f' time : {time}')
        print(f'SubSecond : {SubSecond}')
        print('='*80)
    def packet_parse_0x51(self, data):
        """
        Парсер пакета Калибровки датчика давления
        float ADC2Bridge[4]		A0, AT, B0, BT для формулы ADC24*(A0+AT*T)+(B0+BT*T) -> Bridge [В/В]
        float Bridge2Press[4]		A0, AT, B0, BT для формулы Bridge*(A0+AT*T)+(B0+BT*T) -> Press [Па]
        float Temp			температура
        float Press2Units		коэффициент преобразования давления [Па]->[PUnits]
        """
        pars_data = struct.unpack(f'=ffff',data)
        print(f'Вызван метод packet_parse_0x51 : {data} | {pars_data}')
    def handle_format_while(self, packet_format, data) -> str:
        """по формату пакета вызывает нужный обработчик
            return : возвращает разобранный пакет
        """
        hex_format = f'0x{packet_format:02x}'
        method_name = f"packet_parse_{hex_format}"
        
        handle = getattr(self, method_name, None)
        try:
            if handle:
                result = handle(data)
                
                return result
            else:
                print(f"Неизвестный формат: {hex_format} ({packet_format})")
        except Exception as err:
            print(f'Произошла ошибка в методе {method_name} : {err} | {",".join(str(f'{x:02x}') for x in data)}')
    def handle_format(self, packet_format, iterator, dev_id) -> str:
        """по формату пакета вызывает нужный обработчик
            return : возвращает разобранный пакет
        """
        hex_format = f'0x{packet_format:02x}'
        method_name = f"packet_parse_{hex_format}"
        
        handle = getattr(self, method_name, None)
        try:
            if handle:
                header = bytes(islice(iterator,4))
                
                if len(header) < 4:
                    raise ValueError('Пакет оборван : не удалось прочитать заголовок')
                
                body_size = self.get_size_packet(header)
                
                body = bytes(islice(iterator, body_size))
                if len(body) < body_size :
                    raise ValueError(f"Пакет оборван: ожидалось {body_size} байт тела, получено {len(body)}")
                if len(body) == 0:
                    return None
                    #raise ValueError(f"Пакет пуст:  получено {len(body)}")
                result = handle(body)
                return result
            else:
                print(f"Неизвестный формат: {hex_format} ({packet_format})")
        except Exception as err:
            print(f'Произошла ошибка в методе  {method_name} : {err} : искачал формат {hex_format} | len : {len(body)} |{",".join(str(f'{x:02x}') for x in body)}')
    def get_size_packet(self, header : bytes) -> int:
        #dev_id = header[0]
        token = header[0]
        number_digit_first = header[1:3]
        return header[3] 
    def pars_datetime(self, timestamp_bytes) -> datetime:
        year = int.from_bytes(timestamp_bytes[0:1], byteorder='little') + 2000
        month, day, hour, minute, second, subsecond = timestamp_bytes[1] , timestamp_bytes[2], timestamp_bytes[3], timestamp_bytes[4], timestamp_bytes[5], timestamp_bytes[6]
        BI_dt = datetime.datetime(year, month, day, hour, minute, second, subsecond*10000)
        return BI_dt
    def payload_process_format(self ,payload:bytes, split_need : bool = False) -> str:
        """
        Преобразует payload в hex-строку (байты через запятую).
        Если split_byte задан, перед каждым его вхождением добавляется '\r'.
        """
        try:
            if not split_need:
                return ','.join(f'{b:02x}' for b in payload)
            iterator = iter(payload)
            BI_size_packet = bytes(islice(iterator,2))
            BI_size_packet = struct.unpack(f'=H', BI_size_packet)

            timestamp_bytes = bytes(islice(iterator,7))
            BI_dt = self.pars_datetime(timestamp_bytes)
            line = " BI : "+json.dumps({
                "BI_size_packet":BI_size_packet[0],
                "BI_datetime": BI_dt.isoformat()
            })
            hex_parts = []
            hex_parts.append(line)
            for format_byte in iterator:
                hex_str = f'{format_byte:02x}'
                if split_need and format_byte in valid_split_format:
                    dev_id = bytes(islice(iterator,1))
                    if dev_id[0] in valid_split_deviceId:
                        encoding_packet = self.handle_format(format_byte, iterator, dev_id)
                        if not encoding_packet is None:
                            hex_parts.append(encoding_packet)
                        else:
                            hex_parts.append(f"\t{hex_str}")
                else:
                    hex_parts.append(hex_str)
            return ','.join(hex_parts)
        except Exception as err:
            print(f'Произошла ошибка, при разборе пакета : {err}')
            
    def write_record(self, timestamp: int, payload: bytes, source_bytes_read: int):
        """
        Записывает запись в текущий файл. Если количество прочитанных байт исходного файла
        превышает порог, открывает следующий файл.
        """
        if self._current_file is None or source_bytes_read >= self._next_threshold:
            self._open_new_file()
            while self._next_threshold <= source_bytes_read:
                self._next_threshold += self.bytes_per_file

        dt = datetime.datetime(1,1,1) + datetime.timedelta(microseconds=timestamp/10)
        line = json.dumps({
            "datetime":dt.isoformat(),
            "timestamp": timestamp,
            "payload_length": len(payload),
            "data": self.payload_process_format(bytes(payload), split_need=True),
            "orig": bytes(payload).hex(',')
        }) + '\n'
        self._current_file.write(line.replace(',\\t', '\\t').replace('\\t', '\t'))
        self._current_file.flush()
        self._count_record += 1
    def get_count_record(self):
        return self._count_record
    def close(self):
        if self._current_file:
            self._current_file.close()
            self._current_file = None