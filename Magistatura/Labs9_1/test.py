import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
import seaborn as sb
from scipy.stats import norm
from scipy import stats
from pandas import DataFrame

def main():
    df = pd.read_csv('house_train.csv')
    df_numeric = df.select_dtypes(include=[np.number])

    df_numeric.dropna(inplace=True)
    print(f'средняя цена на дом: {df_numeric["SalePrice"].mean()}')
    
    y = df_numeric['SalePrice']
    X = df_numeric.drop(columns=['SalePrice','1stFlrSF', 'GarageArea', 'GrLivArea', 'GarageYrBlt'])

    # Стандартизация признаков
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Разделение на обучающую и тестовую выборку
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

    degrees = [1,2,3]
    cv_scores = []

    for degree in degrees:
        poly_features = PolynomialFeatures(degree=degree)
        x_poly_train = poly_features.fit_transform(X_train)

        model = LinearRegression()
        
        # Оценка модели с помощью кросс-валидации
        scores = cross_val_score(model, x_poly_train, y_train, cv=5, scoring='r2')
        cv_scores.append(scores.mean())

    # Построение графика валидационной кривой
    plt.figure(figsize=(10, 6))
    plt.plot(degrees, cv_scores, marker='o')
    plt.title('Валидационная кривая')
    plt.xlabel('Степень полинома')
    plt.ylabel('Средний R²')
    plt.xticks(degrees)
    plt.grid()
    plt.show()

    # Определение оптимальной степени полинома
    optimal_degree = degrees[np.argmax(cv_scores)]
    print(f'Оптимальная степень полинома: {optimal_degree}')

    # Обучение модели с оптимальной степенью
    poly_features = PolynomialFeatures(degree=optimal_degree)
    x_poly_train = poly_features.fit_transform(X_train)
    x_poly_test = poly_features.transform(X_test)

    model.fit(x_poly_train, y_train)
    y_pred = model.predict(x_poly_test)

    # Оценка качества модели
    score = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    print(f'Качество модели с оптимальной степенью {optimal_degree}:')
    print(f'R²: {score}, MAE: {mae}, MSE: {mse}, RMSE: {rmse}')

if __name__ == "__main__":
    main()
