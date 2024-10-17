import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier

def generated_date(base_data, coef_water = 0, coef_alumin = 0):
    data = []
    for i in range(10000):
        row = [
            int(base_data[0] + i),
                base_data[1] + np.random.uniform(-500, 500), # NTNC - ближний зонд
                base_data[2] + np.random.uniform(-500, 500), # FTNC - дальний зонд
                base_data[3] + np.random.uniform(-1.0, 1.0), # NTNL - счета ближнего зонда
                base_data[4] + np.random.uniform(-1.0, 1.0)  # FTNL - счета дальнего зонда
        ]
        data.append(row)
    return data


def main():
    base_data = [33913720, 1620.0, 2160.0, 0.0415, 3.3395]
    data_water_full = generated_date(base_data)
    df_water_full = pd.DataFrame(data_water_full, columns=['Time', 'NTNC', 'FTNC', 'NTNL', 'FTNL'])
    df_water_full['Water_height'] = 25 # столбец с высотой воды в см
    df_water_full['Aluminium_Concentration'] = 0 # столбец с концетрацией алюминия в мм
    df_water_full['Res_NTNC_NTNL'] = df_water_full['NTNC'] / df_water_full['NTNL']
    df_water_full['Res_FTNC_FTNL'] = df_water_full['FTNC'] / df_water_full['FTNL']

    data_aluminium_10 = generated_date(base_data)
    df_aluminium_10 = pd.DataFrame(data_aluminium_10, columns=['Time', 'NTNC', 'FTNC', 'NTNL', 'FTNL'])
    df_aluminium_10['Water_height'] = 25
    df_aluminium_10['Aluminium_Concentration'] = 10
    df_aluminium_10['Res_NTNC_NTNL'] = df_aluminium_10['NTNC'] / df_aluminium_10['NTNL']
    df_aluminium_10['Res_FTNC_FTNL'] = df_aluminium_10['FTNC'] / df_aluminium_10['FTNL']

    data_aluminium_20 = generated_date(base_data)
    df_aluminium_20 = pd.DataFrame(data_aluminium_20, columns=['Time', 'NTNC', 'FTNC', 'NTNL', 'FTNL'])
    df_aluminium_20['Water_height'] = 25
    df_aluminium_20['Aluminium_Concentration'] = 20
    df_aluminium_20['Res_NTNC_NTNL'] = df_aluminium_20['NTNC'] / df_aluminium_20['NTNL']
    df_aluminium_20['Res_FTNC_FTNL'] = df_aluminium_20['FTNC'] / df_aluminium_20['FTNL']

    data_aluminium_30 = generated_date(base_data)
    df_aluminium_30 = pd.DataFrame(data_aluminium_30, columns=['Time', 'NTNC', 'FTNC', 'NTNL', 'FTNL'])
    df_aluminium_30['Water_height'] = 25
    df_aluminium_30['Aluminium_Concentration'] = 30
    df_aluminium_30['Res_NTNC_NTNL'] = df_aluminium_30['NTNC'] / df_aluminium_30['NTNL']
    df_aluminium_30['Res_FTNC_FTNL'] = df_aluminium_30['FTNC'] / df_aluminium_30['FTNL']
    
    data_aluminium_25 = generated_date(base_data)
    df_aluminium_25 = pd.DataFrame(data_aluminium_25, columns=['Time', 'NTNC', 'FTNC', 'NTNL', 'FTNL'])
    df_aluminium_25['Water_height'] = 25
    df_aluminium_25['Aluminium_Concentration'] = 25
    df_aluminium_25['Res_NTNC_NTNL'] = df_aluminium_25['NTNC'] / df_aluminium_25['NTNL']
    df_aluminium_25['Res_FTNC_FTNL'] = df_aluminium_25['FTNC'] / df_aluminium_25['FTNL']
    
    data_aluminium_15 = generated_date(base_data)
    df_aluminium_15 = pd.DataFrame(data_aluminium_15, columns=['Time', 'NTNC', 'FTNC', 'NTNL', 'FTNL'])
    df_aluminium_15['Water_height'] = 25
    df_aluminium_15['Aluminium_Concentration'] = 15
    df_aluminium_15['Res_NTNC_NTNL'] = df_aluminium_15['NTNC'] / df_aluminium_15['NTNL']
    df_aluminium_15['Res_FTNC_FTNL'] = df_aluminium_15['FTNC'] / df_aluminium_15['FTNL']
    
    data_aluminium_5 = generated_date(base_data)
    df_aluminium_5 = pd.DataFrame(data_aluminium_5, columns=['Time', 'NTNC', 'FTNC', 'NTNL', 'FTNL'])
    df_aluminium_5['Water_height'] = 25
    df_aluminium_5['Aluminium_Concentration'] = 5
    df_aluminium_5['Res_NTNC_NTNL'] = df_aluminium_5['NTNC'] / df_aluminium_5['NTNL']
    df_aluminium_5['Res_FTNC_FTNL'] = df_aluminium_5['FTNC'] / df_aluminium_5['FTNL']

    print('df_water_full: \n',df_water_full.head(5))
    print('df_aluminium_5: \n',df_aluminium_5.head(5))
    print('df_aluminium_10: \n',df_aluminium_10.head(5))
    print('df_aluminium_15: \n',df_aluminium_15.head(5))
    print('df_aluminium_20: \n',df_aluminium_20.head(5))
    print('df_aluminium_25: \n',df_aluminium_25.head(5))
    print('df_aluminium_30: \n',df_aluminium_30.head(5))


if __name__ == '__main__':
    main()