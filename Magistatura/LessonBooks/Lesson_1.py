import Perceptron as Persept
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from Adaline import AdalineGD

def main():
    df = pd.read_csv('./iris/iris.data', header=None, encoding='utf-8')
    y = df.iloc[0:100, 4].values
    y = np.where(y == 'Iris-setosa', -1, 1)
    X = df.iloc[0:100, [0,2]].values

    plt.scatter(X[:50, 0], X[:50, 1], color='red', marker='o', label='щетинистый')
    plt.scatter(X[50:100, 0], X[50:100, 1], color='blue', marker='x', label='разноцветный')
    plt.xlabel('длина чашелистика [cm]')
    plt.ylabel('длина лепестка [cm]')
    plt.legend(loc='upper left')
    plt.title('график рассеяния')
    # график рассеяния
    plt.show()

    ppn = Persept.Perceptron(eta=0.1, n_iter=10)
    ppn.fit(X,y)
    plt.plot(range(1, len(ppn.errors_) + 1), ppn.errors_, marker='o')
    plt.xlabel('Эпохи')
    plt.ylabel('Колличество обновлений')
    plt.title('график ошиб­ки неправильной классификации относительно количества эпох')
    #  график ошиб­ки неправильной классификации относительно количества эпох
    plt.show()

    plot_decision_regions(X,y,classfier=ppn)
    plt.xlabel('Длина чашелистика [cm]')
    plt.ylabel('Длина лепестка [cm]')
    plt.legend(loc='upper left')
    plt.title('график с областями решений')
    # график с областями решений
    plt.show()

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,4))
    ada1 = AdalineGD(n_iter=10, eta=0.01).fit(X,y)
    ax[0].plot(range(1, len(ada1.cost_) + 1), np.log10(ada1.cost_), markers='o')
    ax[0].set_xlabel('Эпохи')
    ax[0].set_ylabel('log(Сумма квадратичных ошибок)')
    ax[0].set_title('Adaline - скорость обучения 0.01')

    ada2 = AdalineGD(n_iter=10, eta=0.0001).fit(X,y)
    ax[1].plot(range(1, len(ada2.cost_) + 1), ada2.cost_, marker='o')
    ax[1].set_xlabel('Эпохи')
    ax[1].set_ylabel('log(Сумма квадратичных ошибок)')
    ax[1].set_title('Adaline - скорость обучения 0.0001')
    plt.show()

def plot_decision_regions(X, y, classfier, resolution = 0.02):
    # настройка генератора маркеров и карту цветов
    markers = ('s','x', 'o', '4', 4)
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])
    # вывести поверхность решения
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    Z = classfier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.figure(figsize=(8,6))
    plt.contourf(xx1, xx2, Z, alpha=0.3, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    # вывод образцов по классам
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0],y=X[y == cl, 1],alpha=0.8,c=colors[idx],marker=markers[idx],label=cl, edgecolor='black')

    
if __name__ == '__main__':
    main()