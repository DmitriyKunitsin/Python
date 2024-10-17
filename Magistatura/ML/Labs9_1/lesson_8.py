# 8) Изучив приложенный материал, постройте валидационную кривую по различным степеням полиномиальной модели. 
# Определите оптимальную степень полинома, постройте заново регрессионную модель 
# и сравните полученные качественные оценки модели с п. 6.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
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

    # # Определение дисперсии и выбор 5 признаков с набольшей дисперсией 
    # variance = np.var(X_scaled, axis=0)
    # top_variance_indices = np.argsort(variance)[-5:]
    # top_variance_features = X.columns[top_variance_indices]
    # print("5 признаков с наибольшей дисперсией:")
    # # Дисперсия Это отслеживание признаков, чьи значения чаще всего изменяются
    # print(top_variance_features)

    # # Определение корреляции и выбор 5 признаков с наибольшей корреляцией с целевым столбцогм
    # correlation = df_numeric.corr()
    # top_correlation_features = correlation['SalePrice'].nlargest(6).index[1:] # Исключаем SalePrice 
    # print("5 признаков с наибольшей корреляцией с целевым столбцом:")
    # # Корелиаци это связь между признаками, чем выше значение, тем сильнее связь
    # print(top_correlation_features)

    # Разделение на обучающую и тестовую выборку
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

    degrees = [1,2,3,4,5]
    results = []
    for degree in degrees:

        poly_features = PolynomialFeatures(degree=degree)
        # Здесь создаются полиномиальные признаки. 
        # Это означается, что к исходным признакам добавляются их полиномиальные комбинации до указанной степени. 
        # Например, если есть два признака x1 и x2 , то при степени 2 будут добавилены  x₁², x₂² и x₁ ⋅ x₂.
        x_poly_train = poly_features.fit_transform(X_train)
        # fit_transform применяется к обучающей выборке и создает новые полномиальные признаки
        x_poly_test = poly_features.transform(X_test)
        # transform применяется к тестовой выборке и создает те же полиномиальные признаки, но без их обучения(т.е. без изменения параметров)


        model = LinearRegression()
        # Здесь создается объект линейной регрессии и обучается 
        model.fit(x_poly_train, y_train)
        # на полиномиальных признаках из обучающей выборки(x_poly_train) и соответствующих целевых значениях(y_train). 
        # Функция fit обучаается модель, подбирая коэффициенты для линейной регрессии 


        # Функция predict используется для получения предсказаний
        y_pred = model.predict(x_poly_test)
        # на основе тестовой выборки с полиномильными признаками (x_poly_test)
        # Она возвращает предсказанные значения целевой переменной (y_pred)

        # Оценка качества модели
        score = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        
        results.append((degree, score, mae, mse, rmse))

    # Вывод результатов
    for degree, score, mae, mse, rmse in results:
        print(f'Степень: {degree}, R²: {score}, MAE: {mae}, MSE: {mse}, RMSE: {rmse}')
    
    # Построение графика валидационной кривой
    degrees, scores = zip(*[(degree, score) for degree, score, _, _, _ in results])
        
    plt.plot(degrees, scores)
    plt.title("Валидационная кривая")
    plt.xlabel("Степень полинома")
    plt.ylabel("R²")
    plt.xticks(degrees)
    plt.show()

    result_features = PolynomialFeatures(degree=1)
    x_poly_train = result_features.fit_transform(X_train)
    x_poly_test = result_features.transform(X_test)
    
    result_model = LinearRegression()
    result_model.fit(x_poly_train, y_train)

    y_pred_result = result_model.predict(x_poly_test)

    score = r2_score(y_test, y_pred_result)
    mae = mean_absolute_error(y_test, y_pred_result)
    mse = mean_squared_error(y_test, y_pred_result)
    rmse = np.sqrt(mse)
    
    print(f'Оценка качества модели с оптимальной степенью полинома: \nR² : {score}\n MAE : {mae}\n MSE: {mse} \n RMSE: {rmse}')

    data = pd.DataFrame({
        'Оригинальные цены' : y_test,
        'Предсказанные цены' : y_pred_result
    })
    plt.figure(figsize=(10,10))
    
    plt.scatter(data.index, data['Оригинальные цены'], color='red', label='Оригинальные цены')
    plt.scatter(data.index, data['Предсказанные цены'], color='blue', label='Предсказанные цены')
    plt.title('Сравнение оригинальных и предсказанных цен')
    plt.xlabel('Индекс')
    plt.ylabel('Цены')
    plt.grid()
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()