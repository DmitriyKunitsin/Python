import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd


def main():
    #Расчет средневзвешанных значений
    x = [6.0, 1, 2.5, 6, 25.0]
    w = [0.1, 0.2, 0.3, 0.25, 0.15]

    y_with_nan = [10.0, 2, 2.5, math.nan, 5, 26.0]
    wmean = sum(w[i] * x[i] for i in range(len(x))) / sum(w)
    print(f'Расчет средневзвешанного с помощью range: {wmean}')
    wmean_2 = sum(x_ * w_ for (x_,w_) in zip(x,w)) / sum(w)
    print(f'Расчет средневзвешанного с помощью zip: {wmean_2}')
    y,z,w = np.array(x), pd.Series(x), np.array(w)
    wmean_3 = np.average(y, weights=w)
    print(f'Расчет средневзвешанного с помощью np.average для массивово NumPy или серии Pandas: {wmean_3}')
    o = (w * y).sum() / w.sum()
    print(f'Расчет средневзвешанного с помощью поэлементного умножения w * y: {o}')
    w = np.array([0.1, 0.2, 0.3, 0.0, 0.2, 0.1])
    print(f'Расчет средневзвешанного для набора, который содержит nan: {(w * y_with_nan).sum() / w.sum()}')


if __name__ =='__main__':
    main()