## Списки и кортежи упорядочные структуры данных и оба допускают дублирование значений
## Набор отличают от обоих, посколько они неупорядочены и следовательно не допускают дублирования значений
## Набор определяют с помощью фигурных скобок.
set1 = {'apple', 'banana', 'orange'}
print(set1)
print('\n')

set2 = set(('apple', 'banana', 'orange'))
print(set2)
print('\n')

print(type(set1))

## Мы не можем использовать индексы для извлечения элементов любого множеста
## Поскольку множества неупорядочены
## Но можно использорвать конструкции цикла for и while

for item in set1:
    print(item)

print('\n')
# Создаем итератор
iterator = iter(set1)
# Используем цикл while для извлечения элементов
while True:
    try:
            item = next(iterator)# Получаем следующий элемент
            print(item)
    except StopIteration:
# Обрабатываем исключение, когда итератор закончится
        break


### Можно добавлять новые элементы с помощью подпрограммы add()

set1.add('pineapple')
print('\n')
print(set1)
print('\n')

## Можно использовать процедуры remove() или discard() для удаления
## элемента из любого списка
set1.remove('banana')
set1.discard('apple')
## Обе процедуры вызывут ошибки, если мы попытаемся удалить несуществующие элементы
print(set1)
print('\n')

## Объединение множеств
set3 = {1,2,3,4,5}
set4 = {6,7,8,9,10}
set5 = set3.union(set4)
print(set5)
print('\n')

## Сохранение объединения в новом наборе
## небольшой алтернатив сохраняет объединение в четвертом наборе

set4.update(set3)
print(set4, '\n')

## Так же можно удалить все элементы набора
set5.clear()

## Метод difference подсчитывает разницу
set3 = {1,2,3,4,5}
set4 = {6,7,8,9,10}
set5 = set3.difference(set4)
print(set5)
set5.clear()
## Мы можем удалить соответствующие элементы из одного из наборов, используя это
print('\n')
set3 = {1,2,3,4,5}
set4 = {6,7,8,9,10}
set5 = set3.difference_update(set4)
print(set5, '\n')
## Моржно вычислить пересечение 
set3 = {1,2,3,4,5}
set4 = {6,7,8,9,10}
set5 = set3.intersection(set4)
print(set5, '\n')
## можно проверить, является ли набор подмножеством другого набора следующим образом
set2 = {1, 2, 3, 4, 5, 6, 7, 8}
print(set1.issubset(set2))

## Аналогично можно проверить является ли набор надмножестов другого набор
set2 = {1, 2, 3, 4, 5, 6, 7, 8}
print(set1.issuperset(set2))

## Можно проверить, не пересикаются ли два множества(не имеют ли они общих элементов)
set1 = {1,2,3}
set2 = {4,5,6}
print(set1.isdisjoint(set2))

## Симметричная разность между двумя наборами вычисляется следующим образом
set1 = {1,2,3}
set2 = {2,3,4}
set3 = set1.symmetric_difference(set2)
print(set3, '\n')

## Объедингения и переcечения с помощью операторов | и s вычисляется следующим образом
print(set1 | set2, '\n')
print(set1 & set2, '\n')

