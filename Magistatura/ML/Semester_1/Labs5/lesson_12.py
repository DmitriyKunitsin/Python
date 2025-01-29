import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd

def main():
    # Найдем смещение
    x = [8.0, 1, 2.5, 4, 28.0]
    x_with_nan = [10.0, 2, 2.5, math.nan, 5, 26.0]
    n = len(x)
    mean_ = sum(x) / n
    var_ = sum((item - mean_) ** 2 for item in x) / (n - 1)
    std_ = var_ ** 0.5
    skew_ = (sum((item - mean_)**3 for item in x)) * n / (( n - 1) * (n - 2) * std_ ** 3)
    print(f'Расчет смещения на чистом Python: {skew_}')
    z, z_with_nan = pd.Series(x), pd.Series(x_with_nan)
    print(f'Расчет смещения с помощью Pandas: {z.skew()}')
if __name__ == '__main__':
    main()