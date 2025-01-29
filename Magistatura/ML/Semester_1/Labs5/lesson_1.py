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

    mean_1 = sum(x) / len(x)
    print(f'Расчет среднего значения, используя sum и len: {mean_1}')
    mean_2 = statistics.mean(x)
    print(f'Расчет среднего значения, используя встроенные функции статистики Python (statistics.mean(x)): {mean_2}')
    mean_3 = statistics.fmean(x)
    print(f'Расчет среднего значения, используя встроенные функции статистики Python (statistics.fmean(x)): {mean_3}')
    mean_4 = statistics.mean(x_with_nan)
    print(f'Расчет среднего значения, который содержит значения nan,используя встроенные функции статистики Python(statistics.mean(x_with_nan)): {mean_4}')
    mean_5 = np.mean(y)
    print(f'Расчет среднего значения, используя NumPy: {mean_5}')
    np.nanmean(y_with_nan)
    print(f'Расчет среднего значения с помощью NumPy, игнорируя nan:{np.nanmean(y_with_nan)}')
    mean_6 = z.mean()
    print(f'Расчет среднего значения объекта pd.Series: {mean_6}')

    #Расчет средневзвешанных значений
    x = [6.0, 1, 2.5, 6, 25.0]
    w = [0.1, 0.2, 0.3, 0.25, 0.15]



if __name__ =='__main__':
    main()