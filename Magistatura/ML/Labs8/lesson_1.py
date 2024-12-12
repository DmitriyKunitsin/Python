import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import seaborn as sb
from scipy.stats import norm
from scipy import stats
from pandas import DataFrame


def garage_size_label(cars):
    if cars == 0:
        return 'nogarage'
    elif cars == 1:
        return '1-cargarage'
    elif cars == 2:
        return '2-cargarage'
    elif cars == 3:
        return '3-cargarage'
    elif cars == 4:
        return '4-cargarage'
    else:
        return 'other'
def main():
    pd.set_option('display.max_columns', 100)
    df = pd.read_csv('house_train.csv')
    df.drop('Id', axis=1, inplace=True)
    print(df.head())
    print(df.columns)
    print(df.shape)
    print(df.describe().T)
    df.describe()
    print(df['SalePrice'].describe())
    na_number = df.isna().sum()
    print("Колличество пустых значения в наборе данных :\n",na_number)

    duplic_number = df.duplicated().sum()
    print('Повторящиеся строки ( дубликаты ) :\n', duplic_number)

    print('Список названий столбцов :\n', df.columns)

    # Сколько пропущеных значений в параметрах
    na_count = df.isnull().sum().sort_values(ascending=False) 
    # Частота или вероятносить с которй пропущенное 
    # значение встречается в каждом параметрe
    # Если вероятность большая (>0.5), столбы-парамтры можно смело удаляться
    na_rate = na_count / len(df)
    #  массив для печати
    na_data = pd.concat([na_count, na_rate], axis=1, keys=['count', 'ratio'])
    print(na_data)

    df_new = df.drop(['PoolQC', 'MiscFeature', 'Alley'], axis=1)
    print(df_new.isnull().sum())
    
    df_new = df_new.drop(['GarageQual', 'GarageCond', 'Fence'], axis=1)
    print(df_new.isna().sum())
    df_new=df_new.drop(['MasVnrArea', 'MasVnrType'], axis=1)
    print(df_new.isna().sum())
    print('__________________________________')
    print('Размер данных после обработки пропущенного значения : ',df_new.shape)

    df = df_new
    print(df.shape)
    df = pd.read_csv('house_train.csv')
    print(df.head())

    # Гистограмма #
    # sb.displot(df['SalePrice'])
    # plt.show()
    print('Skewness: %f' % df['SalePrice'].skew())

    # plt.figure(figsize=(10,6))
    # sb.histplot(df['SalePrice'], bins=30, kde=True)
    # kde - добавляет кривую плотности
    # plt.title('Histogram of Sale Price')
    # plt.xlabel('Price')
    # plt.ylabel('Count')
    # plt.show()


    # sb.boxplot(df['SalePrice'])
    # plt.title('Box plot of SalePrice')
    # plt.xlabel('SalePrice')
    # plt.show()
    # Построение Boxplot
    # plt.figure(figsize=(10, 5))
    # sb.boxplot(x='CentralAir', y='SalePrice', data=df)
    # plt.title("Boxplot of Sale Price by Air Conditioning")
    # plt.xlabel("Air Conditioning")
    # plt.ylabel("Sale Price")
    # plt.show()

    # Построение гистограмм
    # plt.figure(figsize=(10, 5))
    # sb.histplot(data=df, x='SalePrice', hue='CentralAir', multiple='stack', bins=10)
    # plt.title("Histogram of Sale Price by Air Conditioning")
    # plt.xlabel("Sale Price")
    # plt.ylabel("Frequency")
    # plt.show()

    df['GarageSize'] = df['GarageCars'].apply(garage_size_label)
    plt.figure(figsize=(10,5))
    sb.boxplot(x='GarageSize', y='SalePrice', data=df)
    plt.title("Boxplot of SalePrice by Garage Size")
    # plt.xlabel("Garage Size")
    # plt.ylabel("Sale Price")
    plt.show()


    # print(df.groupby('CentralAir')['SalePrice'].describe())
    # print(df.groupby('GarageCars')['GarageArea'].describe())

    # plt.figure(figsize=(10,5))
    # sb.boxplot(x='no garage', y='Sale price', data=df)







if __name__ == '__main__':
    main()