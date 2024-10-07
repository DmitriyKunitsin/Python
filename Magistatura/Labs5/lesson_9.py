import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd

def main():
    # Мода
    u = [2, 3, 2, 8, 12]
    mode_ = max((u.count(item), item) for item in set(u))[1]
    print(f'Вычисление моды: {mode_}')
    mode_2 = statistics.mode(u)
    print(f'Вычисление моды с помощью statistics.mode(): {mode_2}')
    # mode_3 = statistics.multimode(u)
    # print(f'Вычисление моды с помощью statistics.multimode(): {mode_3}')
    mode_4 = scipy.stats.mode(u)
    print(f'Вычисление моды с помощью scipy.stats.mode(): {mode_4}')


if __name__ == '__main__':
    main()