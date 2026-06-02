import re

def parse_sensor_file(filename):
    """
    Парсит файл с данными датчиков и возвращает массив записей
    """
    records = []
    
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    i = 0
    while i < len(lines):
        # Пропускаем пустые строки
        if not lines[i].strip():
            i += 1
            continue
        
        # Парсим строку с ds18
        ds18_match = re.match(r'ds18:bytearray\(b\'(.*?)\'\)\s+(\d+):(\d+)\s+temp=([\d.]+)', lines[i])
        if ds18_match:
            record = {
                'ds18_id': ds18_match.group(1),
                'hour': int(ds18_match.group(2)),
                'minute': int(ds18_match.group(3)),
                'ds18_temp': float(ds18_match.group(4))
            }
            
            # Проверяем следующую строку с данными dht
            if i + 1 < len(lines):
                dht_match = re.match(r'\s+dht\.temperature\(\)=([\d.]+)\s+dht\.humidity\(\)=([\d.]+)', lines[i + 1])
                if dht_match:
                    record['dht_temp'] = float(dht_match.group(1))
                    record['dht_humidity'] = float(dht_match.group(2))
                    
                    # Добавляем запись в массив
                    records.append(record)
            
            i += 2  # Пропускаем обе строки (ds18 и dht)
        else:
            i += 1
    
    return records

def measere_avg(records, key='ds18_temp'):
    """
    Считает абсолютную погрешность для указанного ключа
    records - массив словарей с данными
    key - по какому полю считать (по умолчанию ds18_temp)
    """
    # Берём только нужные значения из словарей
    values = [record[key] for record in records]
    
    # Среднее значение
    mean = sum(values) / len(values)
    print(f"среднее значение {key} : {mean}")
    # Абсолютные погрешности для каждого
    errors = [abs(x - mean) for x in values]
    
    # Средняя погрешность
    mean_error = sum(errors) / len(errors)
    return mean_error

# Использование
filename = 'temp.txt'  # Замените на имя вашего файла
result = parse_sensor_file(filename)
# Вывод результата для проверки
for record in result:
    print(record)

# Для ds18_temp
print(f"Средняя погрешность ds18: {measere_avg(result, 'ds18_temp')}")
print("\n")
# Для dht_temp
print(f"Средняя погрешность dht: {measere_avg(result, 'dht_temp')}")
print("\n")
# Для dht_humidity
print(f"Средняя погрешность влажности: {measere_avg(result, 'dht_humidity')}")
print("\n")
def compare_sensors_error(records):
    """
    Считает погрешность между ds18_temp и dht_temp
    """
    errors = [abs(record['ds18_temp'] - record['dht_temp']) for record in records]
    mean_error = sum(errors) / len(errors)
    return mean_error

# Использование
print(f"Погрешность между датчиками: {compare_sensors_error(result)}")

def relative_error(records, key='ds18_temp'):
    """
    Считает относительную погрешность для указанного ключа
    """
    values = [record[key] for record in records]
    
    # Среднее значение
    mean = sum(values) / len(values)
    
    # Абсолютные погрешности
    abs_errors = [abs(x - mean) for x in values]
    
    # Относительные погрешности для каждого (в %)
    rel_errors = [(abs_err / mean) * 100 for abs_err in abs_errors]
    
    # Средняя относительная погрешность
    mean_rel_error = sum(rel_errors) / len(rel_errors)
    
    return {
        'mean_value': mean,
        'abs_errors': abs_errors,
        'rel_errors': rel_errors,
        'mean_rel_error': mean_rel_error
    }

# Использование
result = parse_sensor_file(filename)
stats = relative_error(result, 'ds18_temp')

print(f"Среднее значение: {stats['mean_value']:.2f}")
print(f"Средняя относительная погрешность: {stats['mean_rel_error']:.2f}%")

# Для каждого элемента
# for i, (val, rel) in enumerate(zip([r['ds18_temp'] for r in result], stats['rel_errors'])):
#     print(f"Элемент {i+1}: {val} -> относительная погрешность {rel:.2f}%")