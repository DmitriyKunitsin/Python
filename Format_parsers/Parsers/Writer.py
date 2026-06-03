import os

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

    def _open_new_file(self):
        if self._current_file:
            self._current_file.close()
        filename = f"{self.base_name}.part{self._part_number}.{self.ext}"
        path = os.path.join(self.base_dir, filename)
        self._current_file = open(path, 'w', encoding='utf-8')
        self._current_file.write("timestamp,payload_length\n")  # заголовок CSV
        self._part_number += 1
        print(f"Создан новый файл: {path}")

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

        line = f"{timestamp},{len(payload)}\n"
        self._current_file.write(line)
        self._current_file.flush()

    def close(self):
        if self._current_file:
            self._current_file.close()
            self._current_file = None