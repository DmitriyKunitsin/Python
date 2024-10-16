# Возьмите датасет из 8-й лабораторной работы (набор данных о ценах на жилье). 
# Выполните подготовку датасета для последующей работы. 1) 
# Оставьте столбцы с числовыми данными - остальные удалите. 
# Не забудьте удалить столбец с нумерацией строк. Сколько столбцов осталось? 

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
    print(df.dtypes)
    df_numeric = df.select_dtypes(include=[np.number])
    print(df_numeric.head())

    # if 'Unnamed: 0' in df_numeric.columns:
    #     df_numeric = df_numeric.drop(columns=['Unnamed: 0'])

    print(f'Количество оставшихся столбцов: {df_numeric.shape[1]}')

   
   

if __name__ == '__main__':
    main()