# 7) Каждый столбец приведите к единичному масштабу. 
# Определите 5 признаков с наибольшей дисперсией - возьмите их для выполнения следующего пункта.
# 2-й вариант - определите 5 признаков с наибольшей корреляцией с целевым столбцом и их возьмите
# для выполнения следующего задания. Не забудьте масштабировать целевой столбец. 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import seaborn as sb
from scipy.stats import norm
from scipy import stats
from pandas import DataFrame

def main():
    df = pd.read_csv('house_train.csv')
    df_numeric = df.select_dtypes(include=[np.number])

    df_numeric.dropna(inplace=True)
    print(f'средняя цена на дом: {df_numeric["SalePrice"].mean()}')
    # Целевое значение
    y = df_numeric['SalePrice']
    # Признаки
    X = df_numeric.drop(columns=['SalePrice','1stFlrSF', 'GarageArea', 'GrLivArea', 'GarageYrBlt'])

    # Разделение на обучающую. и тестовую выборку
    # random_state, отвечает за индексы, что попадут в выборку 
    X_train , X_test, y_train, y_test = train_test_split(X,y,test_size=0.3, random_state=42)

    print('Размер обучающей выборки: ', X_train.shape)
    print(f'Размер тестовой вывборки: {X_test.shape}')

    # Обучаем модель на выборке
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Предсказание
    y_pred = model.predict(X_test)

if __name__ == '__main__':
    main()