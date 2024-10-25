# 7. Обучите модель LassoCV (установите значение гиперпараметра cv
# самостоятельно). Оцените качество полученной модели.Посмотрите на
# коэффициенты модели. Есть ли коэффициенты равные 0? Что это означает?
# Попробуйте их убрать и построить модель заново. Как изменилось качество
# полученной модели?

from sklearn.pipeline import Pipeline

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LassoCV, RidgeCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def main():
    df = pd.read_csv('house_price.csv')
    df = df.select_dtypes(include=[np.number])
    df.drop(['Id'],axis=1,inplace=True)
    df.dropna(inplace=True)
    y = df['SalePrice']
    X = df.drop(['SalePrice'], axis=1)
    X_train , X_test , y_train, y_test = train_test_split(X, y,test_size=0.3, random_state=42)

    lasso = LassoCV(cv=5)
    lasso.fit(X_train, y_train)

    y_pred = lasso.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("MSE :", mse)
    print("R^2 Score:", r2)

    coef = lasso.coef_
    print("Коэффициенты модели:", coef)
    # Нулевые коэфициенты имеют определенное влияние на предсказание целевой переменной 
    # и если коэф равен 0, то он не добавляет ценности в модель , 
    # а если их еще и много , то может затруднить модель в предсказании
    zero_coef = np.where(coef == 0)[0]
    print("Индексы нулевых коэффициентов:", zero_coef)
    
    # Убираю признаки с нулевыми коэффициентами
    X_reduced = X.iloc[:, zero_coef]

    # Повторно обучаю модель без признаков с нулевыми коэффициентами
    lasso_reduced = LassoCV(cv=5)

    lasso_reduced.fit(X_train.drop(columns=X.columns[zero_coef]), y_train)

    # Оценка новой модели
    y_pred_reduced = lasso_reduced.predict(X_test.drop(columns=X.columns[zero_coef]))
    mse_reduced = mean_squared_error(y_test, y_pred_reduced)
    r2_reduced = r2_score(y_test, y_pred_reduced)
    # После того как убрал 0 индексы  MSE чуть-чуть снизился, а R^2 увеличился
    # Это говорит о том, что улаоение сделало модель чуть-чуть более точной и способной объяснять данные 
    print("Mean Squared Error (reduced):", mse_reduced)
    print("R^2 Score (reduced):", r2_reduced)



if __name__ == '__main__':
    main()