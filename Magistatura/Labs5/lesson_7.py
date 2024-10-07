import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd

def main():
    #среднее геометрическое
    x = [6.0, 1, 2.5, 6, 25.0]

    gmean = 1
    for item in x:
        gmean *= item
    gmean **= 1 / len(x)
    print(f'Вычисление геометрического среднего: {gmean}')
    #gmean_2 = statistics.geometric_mean(x)
    #print(f'Вычисление геометрического среднего с помощью statistics.geometric_mean(): {gmean_2}')
    #gmean_3 = statistics.geometric_mean(x_with_nan)
    #print(f'Вычисление геометрического среднего где есть nan:{gmean_3}')
    scipy.stats.gmean(x)
    print(f'Вычисление геометрического среднего с помощью scipy.stats.gmean(): {scipy.stats.gmean(x)}')


if __name__ == '__main__':
    main()