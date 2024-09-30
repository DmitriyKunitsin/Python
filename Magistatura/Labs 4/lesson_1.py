import pandas as pd
import numpy as np

def main():
    df = pd.read_csv('wr88125.txt', delimiter=';', header=None)
    df.columns = ['index', 'year', 'month', 'day', 'min_t', 'average_t', 'max_t', 'fainfall']
    
    print(df)

if __name__ == '__main__':
    main()