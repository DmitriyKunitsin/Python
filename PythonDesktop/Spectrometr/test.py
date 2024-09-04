def sum_pairs(data):
    """Суммирует пары элементов в списке."""
    temp = []
    for i in range(0, len(data), 2):
        if i + 1 < len(data):  # Проверка на наличие следующего элемента
            temp.append(data[i] + data[i + 1])
        else:
            temp.append(data[i])
    print(f'temp len = {len(temp)}')
    return temp
 
# Основной код
data1 = [1, 2, 3, 4, 5, 6,7, 8, 9, 10, 11, 12,13, 14, 15, 16, 17, 18,19, 20, 21, 22, 23, 24,25, 26, 27, 28, 29, 30,31, 32, 33, 34, 35, 36,37, 38, 39, 40, 41, 42,43, 44, 45, 46, 47, 48]


count = 0
all_data = [data1]
print(f'index = {count}, lenght = {len(all_data)}')
all_data.append(sum_pairs(data1))
count +=1 
print(f'index = {count}, lenght = {len(all_data)}')
all_data.append(sum_pairs(all_data[count]))
count +=1 
print(f'index = {count}, lenght = {len(all_data)}')
all_data.append(sum_pairs(all_data[count]))
count +=1 
print(f'index = {count}, lenght = {len(all_data)}')
all_data.append(sum_pairs(all_data[count]))
count +=1 
all_data.append(sum_pairs(all_data[count]))
print(f'index = {count}, lenght = {len(all_data)}')
count +=1 
all_data.append(sum_pairs(all_data[count]))
print(f'index = {count}, lenght = {len(all_data)}')
print(all_data)
print(f'index = {count}, lenght = {len(all_data)}')
all_data.pop()
print(f'index = {count}, lenght = {len(all_data)}')
count -= 1
all_data.pop()
print(f'index = {count}, lenght = {len(all_data)}')
count -= 1
all_data.pop()
print(f'index = {count}, lenght = {len(all_data)}')
count -= 1
all_data.pop()
print(f'index = {count}, lenght = {len(all_data)}')
count -= 1
all_data.pop()
print(f'index = {count}, lenght = {len(all_data)}')
