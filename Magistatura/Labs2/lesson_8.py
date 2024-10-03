import numpy as np

def resizes_arr( arr , i , j):
    arr_5 = arr.reshape(i,j)
    return arr_5    
def main():
    numbers =  (1, 8, 6, 5, 8, 3) 
    arr_3 = np.array(numbers)

    arr_5 = resizes_arr(arr_3, 2, 3)
    
    min_elents_axis_zero = np.min(arr_5, axis=0)
    print(min_elents_axis_zero)

if __name__ == '__main__':
    main()