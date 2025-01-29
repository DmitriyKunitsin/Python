import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd

def main():
    # Сводка описательной статистики
    x = [-5.0, -1.1, 0.1, 2.0, 8.0, 12.8, 21.0, 25.8, 41.0]
    x_with_nan = [10.0, 2, 2.5, math.nan, 5, 26.0]
    y, y_with_nan =  pd.Series(x), pd.Series(x_with_nan)
    result = scipy.stats.describe(y, ddof=1, bias=False)
    print(f'Сводка описательной статистики с помощью scipy.stats.describe(): {result}')
    result_2 = y.describe()
    print(f'Сводка описательной статистики с помощью метода .describe() в Pandas: {result_2}')
if __name__ == '__main__':
    main()