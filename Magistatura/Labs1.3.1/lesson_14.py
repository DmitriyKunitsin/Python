import numpy as np

def search_value( arr , value):
    return np.isin(value, arr)

def main():
     # Создаем массив чисел от 0 до 10
    numbers = np.arange(10)
    arr_6 = numbers ** 2
    print(arr_6)
    if search_value(arr_6, 49):
        print('Значение 49 в массиве есть')
    else:
        print('Значение 49 в массиве отсутствует')

if __name__ == '__main__':
    main()