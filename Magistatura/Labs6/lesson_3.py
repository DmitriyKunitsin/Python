import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
def confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = sum(data) / len(data)
    se = stats.sem(data)
    h = se * stats.t.ppf((1 + confidence) / 2., n - 1)
    return mean - h, mean + h
def main():
    # Загружаем данные из файла
    df = pd.read_csv('water.txt', sep='\t')
    # 3) доверительные интервалы для средней концентрации кальция в питьевой воде для южных и северных городов
    sourth_hardness = df[df['location'] == 'South']['hardness']
    nourth_hardness = df[df['location'] == 'North']['hardness']

    sourth_hardness_ci = confidence_interval(sourth_hardness)
    nourth_hardness_ci = confidence_interval(nourth_hardness)

    print("\n95% доверительный интервал для средней концентрации кальция:")
    print(f"Южные города: {sourth_hardness_ci}")
    print(f"Северные города: {nourth_hardness_ci}")

if __name__ == '__main__':
    main()