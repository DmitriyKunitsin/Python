import struct

# Пример байтовых данных
data = b'\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00...'

# Функция для распарсивания данных
def parse_data(data):
    parsed_values = []
    
    # Определите размер целого числа (например, 2 байта для int16)
    size_of_int = 1
    
    # Обход данных с шагом по размеру целого числа
    for i in range(0, len(data), size_of_int):
        # Извлечение подстроки и распаковка
        chunk = data[i:i + size_of_int]
        if len(chunk) == size_of_int:
            value = struct.unpack('b', chunk)[0]  # '>h' - big-endian int16
            parsed_values.append(value)
    
    return parsed_values

# Вызов функции
parsed_data = parse_data(data)

# Вывод результатов
print(parsed_data)
