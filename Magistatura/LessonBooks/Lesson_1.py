import Perceptron as Persept
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    plt.show()


if __name__ == '__main__':
    main()