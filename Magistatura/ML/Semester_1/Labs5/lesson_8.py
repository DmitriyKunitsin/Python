import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd

def main():
    # Медиана
    x = [6.0, 1, 2.5, 6, 25.0]
    n = len(x)
    if n % 2:
        median_ = sorted(x)[round(0.5*(n-1))]
    else:
        x_ord, index = sorted(x), round(0.5 * n)
        median_ = 0.5 * (x_ord[index-1] + x_ord[index])
    print(f'Расчет медианы: {median_}')
    median_2 = statistics.median(x)
    print(f'Расчет медианы с помощью statistics.median() : {median_2}')
    statistics.median_low(x[:-1])
    print(f'Расчет медианы с помощью statistics.median_low : {statistics.median_low(x[:-1])}')
    statistics.median_high(x[:-1])
    print(f'Расчет медианы с помощью statistics.median_high : {statistics.median_high(x[:-1])}')
    median_2 = np.median(x)
    print(f'Расчет медианы с помощью np.median: {median_2}')


if __name__ == '__main__':
    main()