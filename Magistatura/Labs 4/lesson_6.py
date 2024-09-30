import pandas as pd
import numpy as np


def main():
    df = pd.read_table('wr88125.txt', delimiter=';')
    df.columns = ['index', 'year', 'month', 'day', 'min_t', 'average_t', 'max_t', 'fainfall']

        # столбцы в числовые значения, заменяя ошибки на NaN
    df['min_t'] = pd.to_numeric(df['min_t'], errors='coerce')
    df['average_t'] = pd.to_numeric(df['average_t'], errors='coerce')
    df['max_t'] = pd.to_numeric(df['max_t'], errors='coerce')
    df['fainfall'] = pd.to_numeric(df['fainfall'], errors='coerce')

    df['date'] = pd.to_datetime(df[['year','month','day']], errors='coerce')

    df['Размах температур'] = df['max_t'] - df['min_t']

    df = df.sort_values('date')
    df['Дни без осадков'] = df['fainfall'].eq(0).cumsum()
    df['Дни без осадков'] = df.groupby((df['fainfall'] != 0).cumsum()).cumcount()
    

    print(df)

if __name__ == '__main__':
    main()