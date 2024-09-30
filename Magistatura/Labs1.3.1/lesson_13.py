import numpy as np

def census_arraye( arr ):
    census_arr = np.copy(arr)
    # срез начинает со 1го и через каждые 2 присваивает
    census_arr[1::2] = 2
    return census_arr

def main():
     # Создаем массив чисел от 0 до 10
    numbers = np.arange(10)
    arr_6 = numbers ** 2
    print(census_arraye(arr_6))

if __name__ == '__main__':
    main()