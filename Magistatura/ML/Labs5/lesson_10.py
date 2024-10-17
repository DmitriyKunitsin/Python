import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd

def main():
    # Расчет дисперсии
    x = [6.0, 1, 2.5, 6, 25.0]
    x_with_nan = [10.0, 2, 2.5, math.nan, 5, 26.0]
    n = len(x)
    mean = sum(x) / n
    var_ = sum((item - mean) ** 2 for item in x) / (n - 1)
    print(f'Оценка дисперсии на чистом Python: {var_}')
    var_1 = statistics.variance(x)
    print(f'Оценка дисперсии с помощью statistics.variance(): {var_1}')
    try:
        statistics.variance(x_with_nan)
        print(f'Оценка дисперсии с помощью statistics.variance(), где есть nan: {statistics.variance(x_with_nan)}')
    except ValueError as e:
        var_nan = str(e)
        print(f'Оценка дисперсии с помощью statistics.variance(), где есть nan: {var_nan}')
    var_2 = np.var(x, ddof=1)
    print(f'Оценка дисперсии, используя NumPy с помощью np.var(): {var_2}')
    x_array = np.array(x)
    var_3 = x_array.var(ddof=1)
    print(f'Оценка дисперсии, используя NumPy с помощью метода .var(): {var_3}')
if __name__ == '__main__':
    main()