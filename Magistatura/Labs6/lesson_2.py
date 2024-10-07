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
    # 2) Доверительный интервал 
    south_mortatily = df[df['location'] == 'South']['mortality']
    north_mortatily = df[df['location'] == 'North']['mortality']

    south_mortatily_ci = confidence_interval(south_mortatily)
    north_mortatily_ci = confidence_interval(north_mortatily)

    print("\n95% доверительный интервал для средней годовой смертности:")
    print(f"Южные города: {south_mortatily_ci}")
    print(f"Северные города: {north_mortatily_ci}")

if __name__ == '__main__':
    main()