import struct
def max_value(data):
        temp = data[0]
        for i in data:
            if temp < i:
                temp = i 
        return temp
# Пример байтовых данных
data =b'''\x00\x08\x00\x10\x00\x08\x00\x0b\x00\x13\x00\x11\x00\x16\x00\x12\x00\x14\x00\x0b\x00\x17\x00\x12\x00\x1b\x00%\x00!\x00+\x00"\x00#\x00\x1d\x00\'\x00(\x00&\x00\'\x00/\x001\x00\'\x00,\x003\x00+\x009\x00-\x003\x00%\x004\x005\x00'''
# Функция для распарсивания данных
def parse_data(data):
    parsed_values = []
    
    # Определите размер целого числа (например, 2 байта для int16)
    size_of_int = 2
    
    # Обход данных с шагом по размеру целого числа
    for i in range(0, len(data), size_of_int):
        # Извлечение подстроки и распаковка
        chunk = data[i:i + size_of_int]
        if len(chunk) == size_of_int:
            value = struct.unpack('<H', chunk)[0]  # '>h' - big-endian int16
            parsed_values.append(value)
    
    return parsed_values

# def my_parse(data):
#     data_list = []
#     two = []
#     res = []
#     for i in range(0, len(data), 2):
#             two_byte = data[i:i+2]
#             data_list.append(two_byte)
#     for i in range(0, len(data_list)):
#         if i + 1 < len(data_list):
#             two.append(data_list[i] + data_list[i+1])
#     for i in two:
#         print(int(i))
#     return res

def parse_data_byte(data):
    data_list = []
    numbers = [int.from_bytes(data[j:j+2], byteorder='little') for j in range(0, len(data), 2)]
    for i in numbers:
        data_list.append(i)
    return data_list
# Вызов функции
parsed_data = parse_data(data)
# byte_data = parse_data_byte(data)
# my_parsed = my_parse(data)
test_data = []
for i in data:
    test_data.append(i)
# print(max_value(parsed_data))
print('Фактические значения ',test_data)
print('Фактическая строка ',data)
print('Распарсено ',parsed_data)


# print(my_parsed)
# Вывод результатов
# for i in range(len(parsed_data)):
#     byte_value = data[i * 2:i * 2 + 2]  # Получаем соответствующие байты
#     print(f'Байты: {byte_value} = Целое: {parsed_data[i]}')
