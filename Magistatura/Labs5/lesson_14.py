import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd

def main():
    # Диапазон данных
    x = [-5.0, -1.1, 0.1, 2.0, 8.0, 12.8, 21.0, 25.8, 41.0]
    x_with_nan = [10.0, 2, 2.5, math.nan, 5, 26.0]
    y, y_with_nan =  pd.Series(x), pd.Series(x_with_nan)
    z, z_with_nan = pd.Series(y), pd.Series(y_with_nan)
    
    np.ptp(y)
    np.ptp(z)
    np.ptp(y_with_nan)
    np.ptp(z_with_nan)
    print(f'Нахождение диапазона с помощью функции np.ptp(): {np.ptp(y),np.ptp(z),np.ptp(y_with_nan),np.ptp(z_with_nan)}')
if __name__ == '__main__':
    main()