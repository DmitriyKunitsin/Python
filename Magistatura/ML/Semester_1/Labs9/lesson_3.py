import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def main():
    # Данные
    x = np.array([10, 12, 15, 20, 25, 30, 34, 40, 47, 54, 57])[:, np.newaxis]
    y = np.array([80, 75, 70, 63, 65, 70, 76, 85, 90, 92, 87])

    # Степени полинома для анализа
    degrees = [2, 5, 15]
    
    # Параметры для графика
    plt.scatter(x, y, color='blue', label='Данные')

    for degree in degrees:
        # Преобразование полинома
        poly_features = PolynomialFeatures(degree=degree)
        x_poly = poly_features.fit_transform(x)

        # Обучение модели
        lr = LinearRegression()
        lr.fit(x_poly, y)

        # Предсказание
        y_pred_poly = lr.predict(x_poly)

        # Отображение линии на графике
        plt.plot(x, y_pred_poly, label=f'Полиномиальная регрессия (степень {degree})')

    # Настройки графика
    plt.title("Полиномиальная регрессия с разными степенями полинома")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()

# Комментарии о результатах:
# 1. Более сложная модель с увеличением степени полинома становится более гибкой и лучше подстраивается под данные.
# 2. Высокая степень полинома может привести к переобучению: модель слишком хорошо подстраивается под обучающие данные, включая шум.
# 3. График становится более извивающимся с увеличением степени полинома.
# 4. Модель с высокой степенью полинома более чувствительна к выбросам данных.
