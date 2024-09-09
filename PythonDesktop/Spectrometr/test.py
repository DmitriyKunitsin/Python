# def sum_pairs(data):
#     """Суммирует пары элементов в списке."""
#     temp = []
#     for i in range(0, len(data), 2):
#         if i + 1 < len(data):  # Проверка на наличие следующего элемента
#             temp.append(data[i] + data[i + 1])
#         else:
#             temp.append(data[i])
#     print(f'temp len = {len(temp)}')
#     return temp
import copy
import matplotlib.pyplot as plt
import numpy as np
def delim_pairs(data):
    ''' Делит каждое значение '''
    temp = []
    for i in range(0 , len(data)):
        if i + 1 < len(data):
            temp.append(data[i] / 2)
        else:
            temp.append(data[i] / 2)
    return temp
def sum_pairs(data):
        """Суммирует пары элементов в списке."""
        temp = []
        for i in range(0, len(data), 6):
            if i + 5 < len(data):  # Проверка на наличие следующего элемента
                step_1 = data[i] + data[i + 1]
                step_2 = data[i + 2] + data[i + 3]
                step_3 = data[i + 4] + data[i + 5]
                # temp.append(data[i] + data[i + 1])
                temp.append(step_1)
                temp.append(step_2)
                temp.append(step_3)
            else:
                temp.append(data[i])
        return temp
# Основной код
data1 = [1, 2, 3, 4, 5, 6,7, 8, 9, 10, 11, 12,13, 14, 15, 16, 17, 18,19, 20, 21, 22, 23, 24,25, 26, 27, 28, 29, 30,31, 32, 33, 34, 35, 36,37, 38, 39, 40, 41, 42,43, 44, 45, 46, 47, 48, 100]

all_data = []
all_data.append(sum_pairs(data1))
print(all_data)
print('\n\n')
all_data.append(sum_pairs(all_data[0]))
print(all_data)
print('\n\n')
all_data.append(sum_pairs(all_data[1]))
print(all_data)
print('\n\n')
all_data.append(sum_pairs(all_data[2]))
print(all_data)
print('\n\n')
all_data.append(sum_pairs(all_data[3]))
print(all_data)
print('\n\n')
all_data.append(sum_pairs(all_data[4]))
print(all_data)
print('\n\n')
all_data.append(sum_pairs(all_data[5]))
print(all_data)
# count = 0
# all_data = [data1]
# print(f'index = {count}, lenght = {len(all_data)}')
# all_data.append(sum_pairs(data1))
# count +=1 
# print(f'index = {count}, lenght = {len(all_data)}')
# all_data.append(sum_pairs(all_data[count]))
# count +=1 
# print(f'index = {count}, lenght = {len(all_data)}')
# all_data.append(sum_pairs(all_data[count]))
# count +=1 
# print(f'index = {count}, lenght = {len(all_data)}')
# all_data.append(sum_pairs(all_data[count]))
# count +=1 
# all_data.append(sum_pairs(all_data[count]))
# print(f'index = {count}, lenght = {len(all_data)}')
# count +=1 
# all_data.append(sum_pairs(all_data[count]))
# print(f'index = {count}, lenght = {len(all_data)}')
# print(all_data)
# print(f'index = {count}, lenght = {len(all_data)}')
# all_data.pop()
# print(f'index = {count}, lenght = {len(all_data)}')
# count -= 1
# all_data.pop()
# print(f'index = {count}, lenght = {len(all_data)}')
# count -= 1
# all_data.pop()
# print(f'index = {count}, lenght = {len(all_data)}')
# count -= 1
# all_data.pop()
# print(f'index = {count}, lenght = {len(all_data)}')
# count -= 1
# all_data.pop()
# print(f'index = {count}, lenght = {len(all_data)}')
# count -= 1
# all_data.pop()
# print(f'index = {count}, lenght = {len(all_data)}')
# count -= 1
# all_data.pop()
# print(f'index = {count}, lenght = {len(all_data)}')
# print('\n\n')
# all_data.append(delim_pairs(data1))
# print(all_data)
print('\n\n')
a = [1,2,3]
b = a # ссылка на объект а
b.append(4)
print('a =',a)
b.pop()

b = copy.copy(a) # поверхностная копия
b.append(4)
print('a =',a)
print('b =',b)

a = [[1, 2], [3, 4]]
b = copy.deepcopy(a) # глубокая копия
b[0].append(5)
print('a =',a)
print('b =',b)

markers = (
    ('.', 'Точки'),
    (',', 'Пиксель'),
    ('o', 'Круг'),
    ('v', 'Треугольник вниз'),
    ('^', 'Треугольник вверх'),
    ('<', 'Треугольник влево'),
    ('>', 'Треугольник вправо'),
    ('1', 'tri_down'),
    ('2', 'tri_up'),
    ('3', 'tri_left'),
    ('4', 'tri_right'),
    ('8', 'Восьмиугольник'),
    ('s', 'Квадрат'),
    ('p', 'Пятиугольник'),
    ('P', 'Плюс залитый'),
    ('*', 'Звезда'),
    ('h', 'Шестиугольник 1'),
    ('H', 'Шестиугольник 2'),
    ('+', 'Плюс'),
    ('x', 'x'),
    ('X', 'x залитый'),
    ('D', 'Ромб'),
    ('d', 'Тонкий ромб'),
    ('|', 'Вертикальная линия'),
    ('_', 'Горизонтальная линия')
)
myid =[]
mymerker = []
mydistrip = []
for  marker, distrip in markers:
    #  myid.append(id)
     mymerker.append(marker)
     mydistrip.append(distrip)

# print(myid)
print(mymerker)
print(mydistrip)

for marker,dis in markers:
     if mydistrip[2] in dis:
          print(marker, dis)



# Пример данных
x = np.arange(10)
y1 = np.array([2000] * 10)
y2 = np.array([45] * 10)

plt.figure()
plt.plot(x, y1, label='Значения 2000')
plt.plot(x, y2, label='Значения 45')

# Установка логарифмической шкалы
plt.yscale('log')

plt.legend()
plt.show()

