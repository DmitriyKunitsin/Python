import numpy as np

def coup_array( arr ):
    coup_arr = np.copy(arr)
    # Срез возвращает массив в обратном порядке
    return coup_arr[::-1]

def main():
    # Создаем массив чисел от 0 до 10
    numbers = np.arange(10)
    arr_6 = numbers ** 2
    # ::2 означает "начать с первого эл-та и брать каждый второй"
    Every_second_elements = arr_6[::2]
    print(Every_second_elements)
    print(coup_array(Every_second_elements))


if __name__ == "__main__":
    main()