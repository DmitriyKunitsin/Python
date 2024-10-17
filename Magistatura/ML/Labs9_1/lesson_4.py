# 4) Отделите признаки и целевой столбец. 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import seaborn as sb
from scipy.stats import norm
from scipy import stats
from pandas import DataFrame

# Признаки(фичи) : Это входные данные, которые вы будут использоваться для предсказания. 
# Например, в задаче предсказания цены дома, 
# признаки могут включать площадь, колличество комнат, наличие гража и т.д.

# Целевой столбец (целевое значение): Это то, что вы хотите предсказать.
# Это цена продажи дома

def main():
    df = pd.read_csv('house_train.csv')
    df_numeric = df.select_dtypes(include=[np.number])

    df_numeric.dropna(inplace=True)
    
    # Целевое значение
    y = df_numeric['SalePrice']
    # Признаки
    X = df_numeric.drop(columns=['SalePrice','1stFlrSF', 'GarageArea', 'GrLivArea', 'GarageYrBlt'])
    # По личному выводу и убеждению с прошлого задания, удаляю столбцы с высокой кориляцией
    print(X.head())
    print(y.head())
    
if __name__ == '__main__':
    main()