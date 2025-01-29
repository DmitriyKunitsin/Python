# 5. Разделите набор данных на входные данные X (все столбцы кроме SalePrice) и ответы y (столбец SalePrice).

from sklearn.pipeline import Pipeline

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split

def main():
    df = pd.read_csv('house_price.csv')
    df = df.select_dtypes(include=[np.number])
    df.drop(['Id'],axis=1,inplace=True)
    df.dropna(inplace=True)
    y = df['SalePrice']
    X = df.drop(['SalePrice'], axis=1)
    X_train , X_test , y_train, y_test = train_test_split(X, y,test_size=0.3, random_state=42)
if __name__ == '__main__':
    main()