## Данные в строках хранятся одинаково, независимо от того, используем ли мы пару одинарных или двойных ковычек
print("Python == Python : ",'Python' == "Python",'\n')
print("Python == python : ",'Python' == "python",'\n')

print('Python')
var1 = 'Python'
print(var1)

## Многострочные строки
var2 = ''' test string,
test string '''
var3 = """ test string,
test string """

## Можно рассматривать строки как массивы
for i in var1:
    print(i)

print('\n')
## Можно вычислить длину строки
print("len(var1) : ",len(var1))
print('\n')

print("'test' in 'This is a test' : ",'test' in 'This is a test')

print("'test' not in 'This is a test' : ",'test' not in 'This is a test')

print('\n')
## Можно разрезать строки так же как списки
var1 = 'This is a test.'
print("var1[2:] : ",var1[2:])

print("var1[2:7] : ",var1[2:7])

print('\n')

## Можно изменить регистр буквенных символов в строке

var1 = 'MiXed CaSe'
print("var1.upper() : ",var1.upper())
print("var1.lower() : ",var1.lower())

## Можно удалить ненужные пробелы с обоих концов строк
var1 = ' whitespace     '
print("' whitespace     ' : ", var1.strip())

## Можно заменить символы в строке

var1 = 'love'
print("love : ", var1.replace('o', '0'))

## Разделить строку вокруг символа
var1 = 'a,b,c,d,e,f'
print("a,b,c,d,e,f : ",var1.split(','))

## Можно использовать первый символ строки с заглавной буквы
var1 = 'hello!'
print("hello! : ", var1.capitalize())

## Можно объединить две строки
var1 = 'Hello, '
var2 = 'World!'
print(var1 + var2)

## Число со строкой объединять нельзя
## Для этого нужно преобразовать числа в строки
age = 28
var1 = 'I am '
print(var1 + str(age))

## Можно отформатировать строку
var1 = 'I am {}'.format(28)
print(var1)
var1 = 'I am {} and my friend is {}'.format(28,29)
print(var1)

print('\n')
## Использование escape-символов
var1 = 'He said, \" I am fine \".'
print(var1)