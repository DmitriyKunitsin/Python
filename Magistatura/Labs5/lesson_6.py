import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd

def main():
    #Гармоническое среднее
    x = [6.0, 1, 2.5, 6, 25.0]
    x_with_nan = [10.0, 2, 2.5, math.nan, 5, 26.0]
    hmean = len(x) / sum(1 / item for item in x)
    print(f'Расчет гармонического среднего: {hmean}')   
    hmean_2 = statistics.harmonic_mean(x)
    print(f'Расчет гармонического среднего с помощью statistics.harmonic_mean(): {hmean_2}')
    print(f'Расчет гармонического среднего, где есть nan: {statistics.harmonic_mean(x_with_nan)}')
    print(f'Расчет гармонического среднего, где есть 0:{statistics.harmonic_mean([1, 0, 2])}')
    print(f'Расчет гармонического среднего с помощью scipy.stats.hmean(): {scipy.stats.hmean(x)}')


if __name__ == '__main__':
    main()