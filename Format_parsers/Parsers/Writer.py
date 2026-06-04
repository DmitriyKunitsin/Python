import os
import json
import datetime
from typing import Optional

valid_split = {0x20, 0x10, 0x40, 0x51, 0x33}

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
        self._current_file.write("timestamp,payload_length\n")  # заголовок CSV
        self._part_number += 1
        print(f"Создан новый файл: {path}")
    def format_payload(payload:bytes, split_need : bool = False) -> str:
        """
        Преобразует payload в hex-строку (байты через запятую).
        Если split_byte задан, перед каждым его вхождением добавляется '\r'.
        """
        hex_parts = []
        
        for b in payload:
            hex_str = f'{b:02x}'
            if split_need and b in valid_split:
                hex_parts.append(f'\r{hex_str}')
            else:
                hex_parts.append(hex_str)
        return ','.join(hex_parts)
    def write_record(self, timestamp: int, payload: bytes, source_bytes_read: int):
        """
        Записывает запись в текущий файл. Если количество прочитанных байт исходного файла
        превышает порог, открывает следующий файл.
        """
        # Если запись первая или достигнут порог — открыть новый файл
        if self._current_file is None or source_bytes_read >= self._next_threshold:
            self._open_new_file()
            # Увеличиваем порог для следующего файла
            while self._next_threshold <= source_bytes_read:
                self._next_threshold += self.bytes_per_file

        # преобразуем байты в строку шестнадцатеричных значений через запятую
        data_str = ','.join(f'{b:02x}' for b in payload) 
        dt = datetime.datetime(1,1,1) + datetime.timedelta(microseconds=timestamp/10)
        line = json.dumps({
            "datetime":dt.isoformat(),
            "timestamp": timestamp,
            "payload_length": len(payload),
            "data": data_str
        }) + '\n'
        self._current_file.write(line)
        self._current_file.flush()
        self._count_record += 1
    def get_count_record(self):
        return self._count_record
    def close(self):
        if self._current_file:
            self._current_file.close()
            self._current_file = None