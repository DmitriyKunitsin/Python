import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def main():
    # Загружаем данные из файла
    df = pd.read_csv('water.txt', sep='\t')

    # 1) Описательные статистики
    print("Описательные статистики для северных городов:")
    print(df[df['location'] == 'North'].describe())
    print("\nОписательные статистики для южных городов:")
    print(df[df['location'] == 'South'].describe())

if __name__ == '__main__':
    main()