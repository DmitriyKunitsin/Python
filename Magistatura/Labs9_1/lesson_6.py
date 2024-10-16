# 6) Обучите модель линейной регрессии и получите оценки качества 
# модели: score, MAE, MSE, RMSE. 
# Определите наиболее значимые признаки по весовым коэффициентам модели.


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

    # Оценка качества модели
    score = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    # Коэфициент детерминации:
    # Это число показвает, насколько хорошо наша модель объясняет данные. 
    # Если R2 близко к 1, значит, модель хорошая, а если близко к 0, то плохая
    print(f'R²: {score}')
    # MAE (Средняя абсолютная ошибка) :
    # Это среднее значение всех ошибок, которые мы сделали в предсказаниях. 
    # Чем меньше MAЕ, тем лучше
    print(f'MAE: {mae}')
    # MSE (Средняя квадратичная ошибка) :
    # Это ошибка, мы возводим каждую ошибка в квадрат перед тем, как средня. 
    # Это помогаем нам больше акцентировать внимание на больших ошибках
    print(f'MSE: {mse}')
    # RMSE (Корень из средней квадратичной ошибки) :
    # Это просто корень из MSE. Он возвращает нас к исходнеым единицами 
    # измерения и помогает понять, насколько в среднем мы ошибаемся
    print(f'RMSE: {rmse}')
    
    # Коэффициенты модели - это числа, которые показывают, как сильно каждый признак(или фактор) 
    # влияет на результат. Например, если мы предсказываем цену дома, то коэффициенты покажут, 
    # насколько цена меняется при изменении площади дома или колличества комнат
    
    # Если коэффициента большой и положительный, это значит, что признак сильно влияет 
    # на увеличение результата. 
    # Если он отрицательный - значит, признак влияет на уменьшение результата 
    coefficients = pd.DataFrame(model.coef_, X.columns, columns=['Coefficient'])
    print(coefficients.sort_values(by='Coefficient', ascending=False))

if __name__ == '__main__':
    main()