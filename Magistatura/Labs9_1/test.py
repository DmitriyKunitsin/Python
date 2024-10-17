import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
import seaborn as sb
from scipy.stats import norm
from scipy import stats
from pandas import DataFrame

def main():
    df = pd.read_csv('house_train.csv')
    df_numeric = df.select_dtypes(include=[np.number])

    df_numeric.dropna(inplace=True)

    plt.scatter(x=df_numeric['SalePrice'], y=df_numeric['Id'], color='red', label='Оригинальные цены')
    plt.show()

if __name__ == "__main__":
    main()
