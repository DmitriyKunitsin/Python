import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd

def main():
    # Расчет среднеквадратичного отклонения:
    x = [6.0, 1, 2.5, 6, 25.0]
    x_with_nan = [10.0, 2, 2.5, math.nan, 5, 26.0]
    n = len(x)
    mean = sum(x) / n
    var_ = sum((item - mean) ** 2 for item in x) / (n - 1)

    std_ = var_ ** 0.5
    print(f'Расчет среднеквадратичного отклонения на чистом Python: {std_}')
    std_2 = statistics.stdev(x)
    print(f'Расчет среднеквадратичного отклонения с помощью statistics.stdev(): {std_2}')
    np.std(x, ddof=1)
    print(f'Расчет среднеквадратичного отклонения с помощью NumPy: {np.std(x, ddof=1)}')

if __name__ == '__main__':
    main()