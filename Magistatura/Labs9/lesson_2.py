import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures  # Класс преобразователь
from sklearn.metrics import mean_squared_error


def main():
    # Задание 2. Постройте полиномиальную модель, описывающую следующую зависимость:
    x = np.array([10, 12, 15, 20, 25, 30, 34, 40, 47, 54, 57])[:, np.newaxis]
    y = np.array([80, 75, 70, 63, 65, 70, 76, 85, 90, 92, 87 ])

    plt.scatter(x, y) # Изображаем точки на графике
    plt.title('Наши точки на графике')
    plt.show()

    lr = LinearRegression()
    lr.fit(x,y)
    poly_features = PolynomialFeatures(degree=2)
    x_poly = poly_features.fit_transform(x)
    lr.fit(x_poly, y)
    y_pred_poly = lr.predict(x_poly)
    plt.scatter(x,y, color='blue', label='Данные')
    plt.plot(x, y_pred_poly, color='green', label='Полиномиальная регрессия')
    plt.title("Полиномиальная регрессия")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()