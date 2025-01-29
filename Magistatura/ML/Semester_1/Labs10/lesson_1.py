from sklearn.pipeline import Pipeline

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def main():
    df = pd.read_csv('house_price.csv')
    print(df.shape[1])
    print('Колличество строк :', df.shape[0])
    print('Колличество столбцов : ', df.shape[1])
    print('Колличество пропусков : \n', df.isnull().sum())
    print(df.info())
    df = df.select_dtypes(include=['int64', 'float64'])
    print(df.info)
    
    

if __name__ == '__main__':
    main()