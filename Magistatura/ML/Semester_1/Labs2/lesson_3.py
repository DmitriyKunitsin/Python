import numpy as np 

def main():
    arr_1 = np.full((3,4), 3)
    arr_2 = np.random.randint(0, 9, (2,4))
    print(f' колличество элементов в массиве arr_1 : {arr_1.size}\n размер массива arr_1 :{arr_1.shape} \n колличество элементов в массиве arr_2 : {arr_2.size}\n размер массива arr_2 : {arr_2.shape}')

if __name__ == '__main__':
    main()