# 4. Удалите столбец Id и пропущенные значения.

from sklearn.pipeline import Pipeline

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def main():
    df = pd.read_csv('house_price.csv')
    df = df.select_dtypes(include=[np.number])
    df.drop(['Id'],axis=1,inplace=True)
    df.dropna(inplace=True)
    print(df.info())
    

if __name__ == '__main__':
    main()