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

    # возвращает количество пропущенных значений для каждого столбца.
    missing_values = df.isnull().sum()
    print("Количество пропущенных значений в каждом столбце:")
    print(missing_values)

if __name__ == '__main__':
    main()