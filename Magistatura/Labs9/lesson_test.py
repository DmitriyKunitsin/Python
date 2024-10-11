import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures  # Класс преобразователь
from sklearn.metrics import mean_squared_error


def main():
    x = np.array([258.0, 270.0, 294.0, 320.0, 342.0, 368.0, 396.0, 446.0, 480.0, 586.0])[:, np.newaxis]
    y = np.array([236.4, 234.4, 252.8, 298.6, 314.2, 342.2, 360.8, 368.0, 391.2, 390.8])
    # plt.scatter(x,y)
    # plt.show()
    # lr = LinearRegression() # Линейная регрессия
    # lr.fit(x,y)
    # x_ = np.arange(250,600,10)[:, np.newaxis] # Точки для предсказания
    # y_lr = lr.predict(x_) # Предсказываем y для линейной регрессии

    # plt.scatter(x,y)
    # plt.plot(x_, y_lr)
    # plt.show()

    # pr = LinearRegression() # Полиномиальная регрессия
    # quadratic = PolynomialFeatures(degree=2)
    # x_quad = quadratic.fit_transform(x) # Преобразуем данные
    # pr.fit(x_quad, y) # Обучаем полиномиальную регрессию

    # y_pr = pr.predict(quadratic.fit_transform(x_)) # Предсказываем y для полиномиальной регрессии

    # plt.scatter(x, y, label = 'тренировочные точки')
    # plt.plot(x_, y_lr, label = 'линейная подгонка')
    # plt.plot(x_, y_pr, label = 'квадратичная подгонка')
    # plt.legend(loc='upper left')
    # plt.show()

    # Задание 1
    # Оцените полученные модели с помощью коэффициента детерминации и MSE. Что можно сказать о качестве моделей?

    lr = LinearRegression()
    lr.fit(x,y)
    y_pred = lr.predict(x)
    print('Для линейной регрессии:', mean_squared_error(y, y_pred))
    poli_features = PolynomialFeatures(degree=2)
    x_poly = poli_features.fit_transform(x)
    lr.fit(x_poly, y)
    y_pred_poly = lr.predict(x_poly)
    print('Для полиномиальной модели :', mean_squared_error(y,y_pred_poly))

    plt.scatter(x,y, color='blue', label='Данные')
    plt.plot(x, y_pred, color='red', label='Линейная регрессия')
    plt.scatter(x, y_pred_poly, color='green', label='Полиномиальная регрессия')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()