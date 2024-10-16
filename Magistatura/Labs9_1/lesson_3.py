# 3) Постройте тепловую матрицу корреляции без учета целевого столбца (цена продажи). 
# Используя метод corr Pandas получите числовую матрицу корреляции признаков. 
# Проведите анализ полученных результатов. 
# Имеет ли смысл какие-то столбцы удалить после проведенного анализа? 
# Укажите 10 признаков с наибольшей корреляцией.

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

    df_numeric = df_numeric_cleaned.drop(columns=['SalePrice'], errors='ignore')

    correlation_matrix = df_numeric.corr()

    plt.figure(figsize=(12,10))
    sb.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', square=True)
    plt.title('Тепловая карта коррелияции')
    plt.show()

    correlation_values = correlation_matrix.abs().unstack().sort_values(ascending=False)
    top_10_correlated = correlation_values[correlation_values < 1].head(10)

    print("10 признаков с наибольшей корреляцией:")
    print(top_10_correlated)

    df_numeric.drop(columns=['1stFlrSF', 'GarageArea', 'GrLivArea', 'GarageYrBlt'], axis=1, inplace=True)
    print(df_numeric.shape[1])

    print('Признаки с корелиацией выше 0.8, считаю, что необходимо удалить, чтоб избежать мультиколлинеарности')

    # Если признаки имеют оченб высокую корреляцию (например, выше 0.8), 
    # это может указывать на то, что их можно рассмотреть для удаления, 
    # чтобы избежаться мультиколлинеарности при построенении модели

    # Корреляция - это связь между двумя вещами. Если они часто меняются вместе, 
    # то мы говорим, что у них высокая корреляция.
    # Если допустим связь у них противоположная (один друг веселится, другой грустит), 
    # то это низкая корреляция

    # Мультиколлинеарность - это ситуация, когда несколько признаков (или факторов)
    #  в данных очень похожи или зависят друг от друга. 
    # Например, если у нас есть информация о росте и весе людей и оба этих признака 
    # показывают одно и то же(высокие люди обычно тяжелее), 
    # это может запутать модель, которую мы строим. 
    # Модель может не понимать, ккой из этих признаков важнее

if __name__ == '__main__':
    main()