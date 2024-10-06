import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd


def main():
    x = [10.0, 2, 2.5, 5, 26.0]
    x_with_nan = [10.0, 2, 2.5, math.nan, 5, 26.0]
    print(f'Вывод исходных данных, которые содержатся в x:{x}')
    print(f'Вывод исходных данных, которые содержатся в x_with_nan:{x_with_nan}')

    y, y_with_nan =  pd.Series(x), pd.Series(x_with_nan)
    z, z_with_nan = np.array(x), np.array(x_with_nan)
    print(f'Вывод данных, которые содержатся в y и y_with_nan:{y},{y_with_nan}')
    print(f'Вывод данных, которые содержатся в z и в z_with_nan: {z},{z_with_nan}')



if __name__ =='__main__':
    main()