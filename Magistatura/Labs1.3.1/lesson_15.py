import numpy as np

def sort_negative_value( arr ):
    negative_arr = arr[arr < 0]
    return negative_arr

def main():
    array = np.random.randint(-10, 10, (4,4))
    print('Исходный массив\n',array)
    print('Отсортированный массив :',sort_negative_value(array))

if __name__ == '__main__':
    main()