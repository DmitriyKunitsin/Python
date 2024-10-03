import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    df = pd.read_table('wr88125.txt', delimiter=';')
    df.columns = ['index', 'year', 'month', 'day', 'min_t', 'average_t', 'max_t', 'fainfall']

    df['min_t'] = pd.to_numeric(df['min_t'], errors='coerce')
    df['average_t'] = pd.to_numeric(df['average_t'], errors='coerce')
    df['max_t'] = pd.to_numeric(df['max_t'], errors='coerce')
    df['fainfall'] = pd.to_numeric(df['fainfall'], errors='coerce')
    df['date'] = pd.to_datetime(df[['year','month','day']], errors='coerce')

    
    # 9.1. Средняя температура воздуха ниже -30°C
    extremal_cold_temperature = df[df['average_t'] < -30]    
    print("\n9.1. Дни со средней температурой ниже -30°C:")
    print(extremal_cold_temperature[['date','average_t']])

    # 9.2. Средняя температура выше 27°C и количество дней без осадков больше 3
    df['Дни без осадков'] = df['fainfall'].eq(0).cumsum()
    df['Дни без осадков'] = df.groupby((df['fainfall'] != 0).cumsum()).cumcount()
    average_temp_and_none_rainfall = df[(df['average_t'] > 27) & (df['Дни без осадков'] > 3)]
    print("\n9.2. Дни со средней температурой выше 27°C и более 3 дней без осадков:")
    print(average_temp_and_none_rainfall[['date', 'average_t', 'Дни без осадков']])



if __name__ == '__main__':
    main()