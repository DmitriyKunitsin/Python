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

    yars_wall_missing = df[df.isnull().any(axis=1)]
    print(yars_wall_missing['year'].value_counts())

if __name__ == '__main__':
    main()