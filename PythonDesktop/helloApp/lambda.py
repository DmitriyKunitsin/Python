
# lambda в Python — это способ создания анонимных функций, 
# то есть функций без имени. 
# Они могут быть полезны в ситуациях, когда вам нужно определить небольшую функцию на месте, 
# не создавая полноценную функцию с использованием ключевого слова def.

# Синтаксис
#   lambda аргументы: выражение

add = lambda x,y: x +y
print(add(2,3))

# Ограниченность:
#   - lambda может содержать только одно выражение и не может включать команды или несколько выражений. 
# Это делает их менее гибкими по сравнению с обычными функциями.

# Сравнение с обычными функциями:
#    - Функции, созданные с помощью def, могут содержать множество выражений и более сложную логику.
#    - Лямбда-функции обычно используются для краткости и простоты.

# Использование:
numbers = [1,2,3,4]
squared = list(map(lambda x: x ** 2, numbers))
print(squared)
# 1. Сортировка:
points = [(1,2), (3,1), (5,0)]
points_sorted = sorted(points, key=lambda point: point[1]) # сортировка по 2 элементу
print(points_sorted)

# 2. Фильтрация:

numbers = [1,2,3,4,5]
even_numbers = list(filter(lambda x : x % 2 == 0, numbers))
print(even_numbers)

# ▎Заключение

# Лямбда-функции — это мощный инструмент для упрощения кода и повышения его читаемости в случаях, 
# когда функции нужны лишь на короткий срок. 
# Однако важно помнить о том, что избыточное использование лямбда-функций может привести к ухудшению читаемости кода.