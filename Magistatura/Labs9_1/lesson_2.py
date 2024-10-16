# 2) Удалите строки с пропущенными данными. Сколько строк осталось?

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import seaborn as sb
from scipy.stats import norm
from scipy import stats
from pandas import DataFrame

def main():
    df = pd.read_csv('house_train.csv')
    df_numeric = df.select_dtypes(include=[np.number])

    before_deleted = df_numeric.shape[0]
    df_numeric_cleaned = df_numeric.dropna()
    remaining_rows = df_numeric_cleaned.shape[0]

    
    print(f'Количество строк до удаления: {before_deleted}')
    print(f'Количество строк с пропущенными данными: {df_numeric.isnull().sum().sum()}')
    print(f'Количество строк после удаления: {remaining_rows}')
   

if __name__ == '__main__':
    main()