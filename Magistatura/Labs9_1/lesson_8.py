# 8) Изучив приложенный материал, постройте валидационную кривую по различным степеням полиномиальной модели. 
# Определите оптимальную степень полинома, постройте заново регрессионную модель 
# и сравните полученные качественные оценки модели с п. 6.
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

    # Стандартизация признаков
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Определение дисперсии и выбор 5 признаков с набольшей дисперсией 
    variance = np.var(X_scaled, axis=0)
    top_variance_indices = np.argsort(variance)[-5:]
    top_variance_features = X.columns[top_variance_indices]
    print("5 признаков с наибольшей дисперсией:")
    # Дисперсия Это отслеживание признаков, чьи значения чаще всего изменяются
    print(top_variance_features)

    # Определение корреляции и выбор 5 признаков с наибольшей корреляцией с целевым столбцогм
    correlation = df_numeric.corr()
    top_correlation_features = correlation['SalePrice'].nlargest(6).index[1:] # Исключаем SalePrice 
    print("5 признаков с наибольшей корреляцией с целевым столбцом:")
    # Корелиаци это связь между признаками, чем выше значение, тем сильнее связь
    print(top_correlation_features)

    # Стандартизация целевого столбца 
    y_scaled = scaler.fit_transform(y.values.reshape(-1, 1)).flatten()

    # Разделение на обучающую и тестовую выборку
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

    print('Размер обучающей выборки: ', X_train.shape)
    print(f'Размер тестовой выборки: {X_test.shape}')

    # Обучение модели линейной регрессии
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Предсказание
    y_pred = model.predict(X_test)

    # Оценка качества модели
    score = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    print(f'R²: {score}')
    print(f'MAE: {mae}')
    print(f'MSE: {mse}')
    print(f'RMSE: {rmse}')

if __name__ == '__main__':
    main()