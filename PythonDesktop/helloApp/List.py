## Список - это упорядоченная структура данных.
## Все элементы список хранятся и извлекаются в определенном порядке
## Самый первый имеет индекс 0. Если размер списка равен n, последний эл-т имеет индекс n-1
fruits_list = ['banana', 'pineapple' , 'orange']

print(fruits_list[0])
print(fruits_list[1])
print(fruits_list[2])

## Можно использовать отрицательный индекс
## -1 относится к последнему элементу
print("\n")
print(fruits_list[-1])
print(fruits_list[-2])

## Длина списка как и в си, функцией len, вместо родной strlen
print("\n")
print(len(fruits_list))

## Тип данных списка функцией type
print("\n")
print(type(fruits_list))

## Можно использовать конструктор list() для создания списка
print("\n")
human = list(('Vanya', 'Dima', 'Vova'))
i = 0
while len(human) > i:
    print(human[i])
    i += 1

## Можно получить диапазон элементов из списка
print("\n")
SBC = ['Raspberry Pi', 'Orange Pi', 'Banana Pi', 'Banana Pro', 'NanoPi',
'Arduino Yun', 'Beaglebone']
## С 2 индекса по 5, т.е. 2,3,4
print(SBC[2:5])
## C 2 индекса, т.е. 2,3,4,5,6
print("\n")
print(SBC[2:])
## До 2 индекса, т.е 0,1
print("\n")
print(SBC[:2])
## С 3 индекса по 6, т.е 3,4,5
print("\n")
print(SBC[-4:-1])

## Конструкция IF
print("\n")
if 'Arduino Yun' in SBC:
    print('Found')
else:
    print('Not Found')

## Можно изменить элемент в списке
print("\n")
SBC[0] = 'Dima'
print(SBC[0])

## Можно вставить элемент в список по индексу
## Элемент с индексом 2 в этом списке сдвигается на одну позицию вперед
## То же самое и с остальными предметами
print("\n")
SBC.insert(2, 'Test insert')
print(SBC[2])

print("\n")

i = 0
while len(SBC) > i:
    print(SBC[i])
    i += 1

## Можно добавить элемент в список следующим образом
print("\n")
## append добавит элемент в конец списка
SBC.append('Test appened')
i = 0
while len(SBC) > i:
    print(SBC[i])
    i += 1

print("\n")
## Можно использовать операцию расширения со списка
## Это добавит один список в конец другого списка
## extend

print( "fruits_list до",fruits_list)
fruits_list.extend(SBC)
i = 0
while len(fruits_list) > i:
    print(fruits_list[i])
    i += 1

print("\n")
print("SBC : " ,SBC)
print( "fruits_list после",fruits_list)

## Можно удалить элемент из списка
## Функцией remove
SBC.remove('Banana Pro')
## Можно удалить разными подходами
print("\n")
print(SBC)
## Если укажем индекс, то он удалит и вернет элемент по индексу
SBC.pop(0)
print(SBC)
## Если не укажет, то он удалит и вытолкнет последний элемент
SBC.pop()
print(SBC)

## Можно удалить все элементы списка
## Функция clear
print("\n")
SBC.clear()
print(SBC)

## Так же можно удалить весь список
del SBC

## Цикл for 
print('\n')
for frut in fruits_list:
    print(frut)

print('\n')
for i in range(len(fruits_list)):
    print(fruits_list[i])

print('\n')

i = 0
while i < len(fruits_list):
    print(fruits_list[i])
    i += 1

## Список смешанных типов 
l4 = [1, 'Test', 'a', 1.2, True , False]

## сортировка списка
## Функция sort
print('\n')
print("До сортировки :", fruits_list)
fruits_list.sort()
print("После сортировки : ", fruits_list)

## сортировка в обратном порядке
print('\n')
fruits_list.sort(reverse= True)
print("сортировка в обратном порядке : ", fruits_list)

## Копирование одного списка в другой
frut = list(('patato', 'avokado'))
## Копирование в новый список
new_list = fruits_list.copy()
print('\n')
## extend() объядиняла два списка
## можно использовать оператор (+)
new_fruit = fruits_list + frut
print(new_fruit)

print('\n')

## Можно использовать оператор умножения со списками
frut = frut * 3
print(frut)