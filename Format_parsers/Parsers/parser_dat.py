import os
import struct
from typing import List, Tuple, Optional
import sys

FILE_FORMAT = ".dat"

class FormatDatParser:
    """Парсер бинарных файлов, записанных методом SaveResponseData."""

    # Константы структуры
    MARKER_x40 = 0x40
    MARKER_x64 = 0x64
    MARKER_A5 = b'\xa5'        # маркер конца записи (1 байт)
    RECORD_MARKER_LEN = len(MARKER_A5)
    TIMESTAMP_LEN = 8
    CRC16_LEN = 2
    LEN_FIELD_SIZE = 2             # размер поля длины (ushort, 2 байта)

    def __init__(self, title: str, path_file: str):
        self._file_format = FILE_FORMAT
        self._title = ""
        self._path_file = ""

        self.title = title
        self.path_file = path_file

    @property
    def file_format(self) -> str:
        return self._file_format

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Название должно быть непустой строкой")
        self._title = value

    @property
    def path_file(self) -> str:
        return self._path_file

    @path_file.setter
    def path_file(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Путь к файлу должен быть непустой строкой")
        self._path_file = value

    @property
    def description(self) -> str:
        return f"Парсер формата {self._file_format}, описание: {self._title}"
    def file_size(self) -> int:
        """Возвращает размер файла в байтах."""
        self._ensure_file_ready()
        return os.path.getsize(self._path_file)
    def _ensure_file_ready(self):
        if not os.path.isfile(self._path_file):
            raise FileNotFoundError(f"Файл не найден: {self._path_file}")
        if not os.access(self._path_file, os.R_OK):
            raise PermissionError(f"Нет прав на чтение: {self._path_file}")
    
    def show_file_header(self, num_bytes: int = 64):
        """Выводит первые num_bytes файла в hex для анализа."""
        self._ensure_file_ready()
        with open(self._path_file, 'rb') as f:
            data = f.read(num_bytes)
        hex_str = ' '.join(f'{b:02x}' for b in data)
        print(f"Первые {len(data)} байт файла:\n{hex_str}")
    # packet = \x40 [длина ответа](2 байта) \x64 [ответ](n байт) [CRC16](2 байта) [Маркер конца посылки](1 байт) [TimeStamp] (8 байт) 1 + 2 + N + 2 + 1 + 8 = 14 + N
    def read_file(self, show_progress_bar : bool = False) -> List[Tuple[int, bytes]]:
        records = []
        print(f'Читается файл : {self._path_file}')
        total_size = os.path.getsize(self.path_file) # Для прогресс бара
        sys.stderr.write('Процесс : 0% - чтение начато\n')
        with open(self._path_file, 'rb') as file:
            while True:
                try:
                    if show_progress_bar:
                        current_pos = file.tell()
                        percent = (current_pos/total_size) * 100 if total_size else 100
                        sys.stderr.write(f'Процесс : {percent:.1f}% : ({current_pos}/{total_size}) \n')
                        sys.stderr.flush()
                    # 1. Ищем стартовый маркер 0x40
                    while True:
                        byte = file.read(1)
                        if not byte:
                            sys.stderr.write('Процесс : 100% - чтение завершено. \n')
                            return records  # EOF
                        if byte[0] == self.MARKER_x40:
                            break
                    # 2. размер (2 байта)
                    size_bytes = file.read(2)
                    if len(size_bytes) < 2:
                        break  # неполная запись в конце
                    size_packet = struct.unpack('<H', size_bytes)[0]
                    if size_packet <= 0:
                        continue

                    # 3. Читаем и проверяем маркер 0x64
                    marker = file.read(1)
                    if not marker or marker[0] != self.MARKER_x64:
                        print("возвращаемся к поиску 0x40")
                        continue  # возвращаемся к поиску 0x40

                    # 4. Читаем payload
                    payload = file.read(size_packet)
                    if len(payload) < size_packet:
                        print("возвращаемся к поиску 0x40")
                        continue

                    # 5. Читаем CRC16 (2 байта)
                    crc = file.read(2)

                    # 6. Читаем и проверяем завершающий маркер 0xA5
                    end_marker = file.read(1)
                    if not end_marker or end_marker != self.MARKER_A5: # не пустой маркер и соответствует шаблону
                        continue

                    # 7. Читаем timestamp (8 байт)
                    ts_bytes = file.read(8)
                    if len(ts_bytes) < 8:
                        continue
                    timestamp = struct.unpack('<q', ts_bytes)[0]
                    # Запись корректна
                    records.append((timestamp, payload))

                except (IndexError, struct.error) as e:
                    # При любой ошибке — продолжаем искать следующий стартовый маркер
                    continue
        return records