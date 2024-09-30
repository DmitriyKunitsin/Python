import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    df = pd.read_table('wr88125.txt', delimiter=';')
    df.columns = ['index', 'year', 'month', 'day', 'min_t', 'average_t', 'max_t', 'fainfall']

        # столбцы в числовые значения, заменяя ошибки на NaN
    df['min_t'] = pd.to_numeric(df['min_t'], errors='coerce')
    df['average_t'] = pd.to_numeric(df['average_t'], errors='coerce')
    df['max_t'] = pd.to_numeric(df['max_t'], errors='coerce')
    df['fainfall'] = pd.to_numeric(df['fainfall'], errors='coerce')

    df['date'] = pd.to_datetime(df[['year','month','day']], errors='coerce')

    yarly_stats = df.groupby('year').agg(
        average_temperature=('average_t', 'mean'),
        total_fainfall=('fainfall', 'sum')
    ).reset_index()

    average_temperature_series = yarly_stats.set_index('year')['average_temperature']
    total_fainfall_serial = yarly_stats.set_index('year')['total_fainfall']

    print('средняя температура в году : ',average_temperature_series)
    print('Общее колличество осадков в году : ',total_fainfall_serial)
    print('Самый теплый год : ', average_temperature_series.idxmax())
    print('Самый холодный год : ', average_temperature_series.idxmin())
    print('Выпало самое большое колличество осадков : ', total_fainfall_serial.idxmax())
    print('Выпало самое наименьшее колличество осадков : ', total_fainfall_serial.idxmin())
    
    plt.figure(figsize=(12,6))
    average_temperature_series.plot(title='Среднегодовая температура')
    plt.ylabel('  Teмпература (*С)')
    plt.show()

    plt.figure(figsize=(12,6))
    total_fainfall_serial.plot(title='Годовое колличество осадков')
    plt.ylabel('Колличество осадков  (мм)')
    plt.show()

if __name__ == '__main__':
    main()