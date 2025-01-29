import numpy as np

def multiply_arrays( arr ):
    temp_arr = np.copy(arr)
    i = 0
    while i < temp_arr.size:
        temp_arr[i] = (temp_arr[i] * 3) + 1
        i += 1
    return temp_arr   
def main():
    numbers =  (1, 8, 6, 5, 8, 3) 
    arr_3 = np.array(numbers)
    arr_4 = multiply_arrays(arr_3)
    print(f'arr_3 : {arr_3}')
    print(f'arr_4 : {arr_4}')

if __name__ == '__main__':
    main()