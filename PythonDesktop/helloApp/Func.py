def func1():
    print('Test')

def main():
    print('This is the main() function block...')
    func1()
    print_msg_one_arg('Test String...')
    print_msg_second_arg("Test String", 5)
    print_msg_defoult("Defoult arg")
    print('\n')
    print(add(5,11))
    (r1, r2) = compute(3,5)
    print(r1)
    print(r2)

def print_msg_one_arg(msg):
    print(msg)

def print_msg_second_arg(msg, count):
    for i in range(count):
        print(f"i = {i}",msg)

## Можно иметь значение аргумента по умолчанию
def print_msg_defoult(msg, count = 2):
    print('\n')
    for i in range(count):
        print("i = {i}", msg)
## Функция возвращающая одно значение
def add(a,b):
    return a + b

## Функция возвращающая несколько значений
def compute(a,b):
    return (a + b, a - b)

if __name__ == "__main__": ## Проверяет, выполняем ли мы модуль напрямую или вызываем его из другой программы Python
    main() ## Если мы запусттим код напрямую, он запустит код, указаный под ним

