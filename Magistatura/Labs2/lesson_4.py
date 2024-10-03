import numpy as np

def main():
    arr_1 = np.full((3,4), 3)
    arr_2 = np.random.randint(0, 9, (2,4))

    combinated_arr = np.concatenate((arr_1, arr_2) , axis=0)
    print(f'Объединенный массив:\n{combinated_arr}')
if __name__ == '__main__':
    main()