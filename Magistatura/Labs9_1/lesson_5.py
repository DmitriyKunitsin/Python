# 5) Разбейте на два множества - для обучения и для тестирования (70/30).
# 70% - для обучения
# 30% - для тестирования

# Обучающая выборка - это часть данных, на которой модель будет обучааться. 
# Она будет использоваться для нахождения закономерностей данных

# Тестовая выборка - это часть данных, которая не использовалась в процессе обучения. 
# Она нужна для проврка качества работы модели на новых, невидимых данных

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

    df_numeric.dropna(inplace=True)
    
    # Целевое значение
    y = df_numeric['SalePrice']
    # Признаки
    X = df_numeric.drop(columns=['SalePrice','1stFlrSF', 'GarageArea', 'GrLivArea', 'GarageYrBlt'])

    # Разделение на обучающую. и тестовую выборку
    X_train , X_test, y_train, y_test = train_test_split(X,y,test_size=0.3, random_state=42)

    print('Размер обучающей выборки: ', X_train.shape)
    print(f'Размер тестовой вывборки: {X_test.shape}')

    
if __name__ == '__main__':
    main()