import numpy as np

def resizes_arr( arr , i , j):
    arr_5 = arr.reshape(i,j)
    return arr_5    

def middle_arif( arr ):
    sum = 0
    for i in arr:
        for j in i:
            sum += j
    sum = sum / arr.size
    return sum
def main():
    numbers =  (1, 8, 6, 5, 8, 3) 
    arr_3 = np.array(numbers)

    arr_5 = resizes_arr(arr_3, 2, 3)

    result = middle_arif(arr_5)
    print(result)

if __name__ == '__main__':
    main()