# 8. Попробуйте использовать L2-регуляризацию, т.е. обучите модель RidgeCV.
# Сравните полученный результат LassoCV и RidgeCV.

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

    y_pred_lasso = lasso.predict(X_test)
    mse = mean_squared_error(y_test, y_pred_lasso)
    r2 = r2_score(y_test, y_pred_lasso)

    print("MSE :", mse)
    print("R^2 Score:", r2)

    coef = lasso.coef_
    print("Коэффициенты модели:", coef)
    
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
    
    print("Mean Squared Error (reduced):", mse_reduced)
    print("R^2 Score (reduced):", r2_reduced)

    # Обучаю RidgeCV
    ridge = RidgeCV(cv=5)
    ridge.fit(X_train, y_train)

    y_pred_ridge = ridge.predict(X_test)
    mse_ridge = mean_squared_error(y_test, y_pred_ridge)
    r2_ridge = r2_score(y_test, y_pred_ridge)

    print("MSE Ridge:", mse_ridge)
    # MSE меньше, значит делает более точные предсказания
    print("R^2 Score Ridge:", r2_ridge)
    # R^2 выше, она объясняет большую долю вариации в данных. Это так же указывает, что Ridge лучше подоходит

    # Почему Ridge лучше? 
    #  ----     Регуляризация : Ridge использует L2-регуляризацию, которая штрафует большие коэффициенты, но не обнуляет их. 
    # Это можнт помочь сохранить большее колличество данных, что особенно полезно, когда в данных много взаимосвязанных признаков 
    #  ----     Многообразие признаков : Если в наборе данных много признаков, которые могут быть взаимосвязаны, 
    # Ridge может лучше справляться с этой многомерностью, поскольку он не отбрасывает признаки, как это делает Lasso
    #  ----     Чувствительность к выбору признаков: Lasso может быть более чувствительным к выбору признаков и может игнорировать 
    # важные признаки, если они коррелируют с другими. Ridge, в свою очередь, учитывает все признаки в расчетах


if __name__ == '__main__':
    main()