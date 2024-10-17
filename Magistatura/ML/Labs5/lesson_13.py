import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd

def main():
    # Процентили
    x = [-5.0, -1.1, 0.1, 2.0, 8.0, 12.8, 21.0, 25.8, 41.0]
    x_with_nan = [10.0, 2, 2.5, math.nan, 5, 26.0]
    y, y_with_nan =  pd.Series(x), pd.Series(x_with_nan)
    print(f'Расчет процентилей с помощью statistics.quantiles(): {statistics.quantiles(x, n=2)}')
    statistics.quantiles(x , n=4, method='inclusive')
    print(f"Расчет процентилей с помощью statistics.quantiles(): {statistics.quantiles(x, n=4, method='inclusive')}")
    y = np.array(x)
    np.percentile(y, 5)
    print(f'Нахождение 5 процентиля : {np.percentile(y, 5)}')
    np.percentile(y, 95)
    print(f'Нахождение 95 процентиля : {np.percentile(y, 95)}')
    z, z_with_nan = pd.Series(y), pd.Series(y_with_nan)
    z.quantile(0.05)
    print(f'Нахождение процентиля используя метод .quantile(): {z.quantile(0.05)}')
if __name__ == '__main__':
    main()