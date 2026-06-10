import os
import struct
from typing import List, Tuple, Optional
import sys
from Parsers.Writer import FileSplitWriter

FILE_FORMAT = ".dat"
SIZE_MEGABYTE = 1
STEP_SIZE = SIZE_MEGABYTE * 1024 * 1024 # Порог срабатывания для начала создания нового файла
STEP_PERCENT = 1
START_SEQUENCE = b'\x40\x00\x00\x64\x00\x00'


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

    START_SEQUENCE = b'\x40\x00\x00\x64\x00\x00' # сигнатура начала посылки
    OFFSET_SEQUENCE = 4 # сдвиг на длину сигнатуры до начала ответа
    BLOCK_READ_SIZE = 24 * 1 # Блок данных чтения за раз
    
    
    
    def __init__(self, title: str, path_file: str):
        self._file_format = FILE_FORMAT
        self._title = ""
        self._path_file = ""
        self._dir_path = os.path.dirname(path_file)
        self._pos_len_packet_dict = dict()
        
        self.title = title
        self.path_file = path_file
    
    @property
    def pos_len_packet_dict(self) -> dict:
        """Возвращает копию словаря (смещение : длина пакета)"""
        return self._pos_len_packet_dict
    
    @property
    def dir_path(self) -> str:
        return self._dir_path

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
    @staticmethod
    def get_format_size(size_bytes: int) -> str:
        """Возвращает размер в читаемом виде: КБ (< 1 МБ), МБ (< 1 ГБ) или ГБ."""
        if size_bytes < 1024:
            return f"{size_bytes} Б"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} КБ"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} МБ"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} ГБ"
    def show_file_header(self, num_bytes: int = 64):
        """Выводит первые num_bytes файла в hex для анализа."""
        self._ensure_file_ready()
        with open(self._path_file, 'rb') as f:
            data = f.read(num_bytes)
        hex_str = ' '.join(f'{b:02x}' for b in data)
        print(f"Первые {len(data)} байт файла:\n{hex_str}")
    
    def build_packet_index(self, 
            show_progress_bar: bool = False,
            writer: Optional[FileSplitWriter] = None) -> dict:
        """
        Сканирует файл и строит индекс пакетов.

        Проходит по всему бинарному файлу, находит все сигнатуры START_SEQUENCE,
        для каждой извлекает длину полезной нагрузки и сохраняет в словарь.

        Returns:
            dict: {смещение_после_сигнатуры (int): длина_payload (int)}

        Note:
            Смещение отсчитывается от начала служебного заголовка (сразу после START_SEQUENCE).
            Словарь кэшируется в self._pos_len_packet_dict и доступен через свойство pos_len_packet_dict.
        """
        print(f'Читается файл : {self._path_file}')
        if show_progress_bar:
            sys.stderr.write(f'Процесс : 0% - Разбора на индексы начат. Рубеж: {self.get_format_size(STEP_SIZE)}\n')
        overlap = len(START_SEQUENCE) - 1
        with open(self._path_file, 'rb') as file:
            offset = 0
            prev_tail = b''
            
            while True:
                block = file.read(self.BLOCK_READ_SIZE)
                if not block:
                    break
                cnt_block+=1
                search_data = prev_tail + block
                pos = 0
                while True:
                    pos = search_data.find(START_SEQUENCE, pos)
                    if pos == -1: # Если совпадений не найдено с pos 
                        break
                    abs_pos = offset + pos + self.OFFSET_SEQUENCE - len(prev_tail)
                    
                    #### Чтение длины ответа
                    # 1. Сохраняю текущий указатель в файле
                    temp_pos = file.tell()
                    # 2. Перемещаюсь по нужному указателю
                    file.seek(abs_pos)
                    # 3. Получаю хедер посылки от БИ
                    header = file.read(4)
                    # 4. Проверка, что валидно всё
                    if len(header) == 4 and header[0] == 0x40 and header[3] == 0x64:
                    # 5. Получаю размер пакета в ответе
                        payload_len = writer.get_size_packet(header)
                        self._pos_len_packet_dict[abs_pos+self.OFFSET_SEQUENCE] = payload_len
                    # 6. Возвращаю указатель туда где взял
                    file.seek(temp_pos)                    
                    ### Конец
                    pos += 1
                offset += len(block)
                if len(block) >= overlap:
                    prev_tail = block[-overlap:]
                else:
                    prev_tail = block
        return self._pos_len_packet_dict
    
    def parse_packets_by_index(self, 
                           show_progress_bar: bool = False,
                           writer: Optional[FileSplitWriter] = None) -> List[dict]:
        """
        Разбирает пакеты, используя ранее построенный индекс.

        Для каждой записи из self._pos_len_packet_dict перемещается по файлу,
        читает заголовок и полезную нагрузку, собирает структурированные данные.

        Args:
            show_progress_bar: Включать ли отображение прогресса.
            writer: Опциональный потоковый писатель для сохранения результатов на лету.

        Returns:
            List[dict]: Список разобранных пакетов. Каждый пакет — словарь с ключами:
                - 'offset': смещение в файле
                - 'timestamp': datetime
                - 'payload': bytes
                - 'length': int

        Raises:
            RuntimeError: Если индекс не был построен (словарь пуст).
        """
        records = [] 
        total_size = os.path.getsize(self._path_file)
        if show_progress_bar:
            sys.stderr.write(f'Процесс : 0% - чтение начато. Рубеж: {self.get_format_size(STEP_SIZE)}\n')
        for index, lenght in self._pos_len_packet_dict.items():
            with open(self._path_file, 'rb') as file:
                try :
                    file.seek(index)
                    payload = file.read(lenght)
                    crc = file.read(2)
                    end_marker = file.read(1)
                    ts_bytes = file.read(8)
                    timestamp = struct.unpack('<q', ts_bytes)[0]
                    current_source_pos = file.tell()
                    if writer:
                        writer.write_record(timestamp, payload, current_source_pos)
                    records.append((timestamp, payload))
                    if show_progress_bar:
                            percent = (current_source_pos / total_size) * 100 if total_size else 100
                            if percent >= step_percent:
                                sys.stderr.write(
                                    f'Процесс : {percent:.1f}% '
                                    f'({self.get_format_size(current_source_pos)}/'
                                    f'{self.get_format_size(total_size)})\n'
                                )
                                step_percent += STEP_PERCENT
                except (IndexError, struct.error):
                    continue
        return records
                    
    
    def read_file(
    self,
    show_progress_bar: bool = False,
    writer: Optional[FileSplitWriter] = None
    ) -> List[Tuple[int, bytes]]:
        """
        Читает все записи. Если writer передан, записи передаются в него немедленно,
        и метод возвращает пустой список (или количество записей). Иначе возвращает список.
        """
        records = [] #if writer is None else None  # если writer, список не нужен
        print(f'Читается файл : {self._path_file}')
        total_size = os.path.getsize(self._path_file)

        if show_progress_bar:
            sys.stderr.write(f'Процесс : 0% - чтение начато. Рубеж: {self.get_format_size(STEP_SIZE)}\n')

        cnt_error_BUG = 0
        valid_sequence = False
        cnt_byte_in_packet = 0
        step_percent = 0
        test = []
        with open(self._path_file, 'rb') as file:
            while True:
                try:
                    # 1. Поиск стартового маркера 0x40
                    while True:
                        byte = file.read(1)
                        cnt_byte_in_packet+=1
                        if not byte:
                            if show_progress_bar:
                                sys.stderr.write('Процесс : 100% - чтение завершено. EOF\n')
                            if writer:
                                writer.close()
                            return records
                        if byte[0] == self.MARKER_x40:
                            break
                    # 2. Размер пакета
                    size_bytes = file.read(2)
                    if len(size_bytes) < 2:
                        break
                    size_packet = struct.unpack('<H', size_bytes)[0]
                    if size_packet <= 0:
                        continue
                    # 3. Маркер 0x64
                    marker = file.read(1)
                    if not marker or marker[0] != self.MARKER_x64:
                        continue

                    # 4. Payload
                    payload = file.read(size_packet)
                    if len(payload) < size_packet:
                        continue

                    # 5. CRC (пропускаем)
                    crc = file.read(2)
                    # 6. Маркер 0xA5
                    end_marker = file.read(1)
                    
                    if not end_marker or end_marker != self.MARKER_A5:
                        continue
                    # 7. Timestamp
                    ts_bytes = file.read(8)
                    if len(ts_bytes) < 8:
                        continue
                    timestamp = struct.unpack('<q', ts_bytes)[0]

                    current_source_pos = file.tell()  # позиция после прочитанной записи
                    if writer:
                        writer.write_record(timestamp, payload, current_source_pos)
                    records.append((timestamp, payload))
                    # if len(records) > 0:
                    #     break
                    # Прогресс-бар
                    if show_progress_bar:
                        percent = (current_source_pos / total_size) * 100 if total_size else 100
                        if percent >= step_percent:
                            sys.stderr.write(
                                f'Процесс : {percent:.1f}% '
                                f'({self.get_format_size(current_source_pos)}/'
                                f'{self.get_format_size(total_size)})\n'
                            )
                            step_percent += STEP_PERCENT
                except (IndexError, struct.error):
                    continue
                
        return records