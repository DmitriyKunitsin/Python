import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import os 
import datetime
import numpy as np

def save_dateframe_to_csv(df, folder_name , prefix):
    os.makedirs(folder_name, exist_ok=True) # Создание папки, если она не существует
    timestamp = datetime.datetime.now().strftime("%d_%m_%Y___%H_%M_%S")
    file_name = f'{prefix}_{timestamp}.csv'
    file_path = os.path.join(folder_name, file_name)
    df.to_csv(file_path, index=False)
    print(f"Файл сохранен: {file_path}")


def clamp(value, min_value=0):
    """Ограничивает значение минимальным порогом."""
    return max(value, min_value)

def calculate_values(base_data, coef_alumin, trnp_value):
    """Вычисляет NTNC, FTNC, NTNL и FTNL значения."""
    NTNC_value = base_data[1] * abs(coef_alumin) / trnp_value
    FTNC_value = base_data[2] * abs(coef_alumin) / trnp_value
    
    FTNC_value = np.random.uniform(FTNC_value - 0.1, FTNC_value + 15)
    NTNC_value = np.random.uniform(NTNC_value - 100, NTNC_value + 250)

    NTNL_value = clamp(NTNC_value / 36023)
    FTNL_value = clamp(FTNC_value / 592)

    return NTNC_value, FTNC_value, NTNL_value, FTNL_value

def generated_date(base_data, coef_alumin=0):
    base_trnp = 100
    data = []
    start_date = pd.Timestamp('2024-10-17')
    for i in range(5000):
        trnp_value = base_trnp - (abs(coef_alumin) * 1.5)
        
        NTNC_value, FTNC_value, NTNL_value, FTNL_value = calculate_values(base_data, coef_alumin, trnp_value)
        time_in_seconds = (base_data[0] + i) / 1000
        timestamp = start_date + pd.to_timedelta(time_in_seconds, unit='s')
        row = [
            timestamp,
            base_data[1] + NTNC_value,  # NTNC - ближний зонд
            base_data[2] + FTNC_value,  # FTNC - дальний зонд
            NTNL_value,                 # NTNL - счета ближнего зонда
            FTNL_value,                 # FTNL - счета дальнего зонда
            clamp(np.random.uniform(abs(trnp_value) - 5, abs(trnp_value) + 5), 0.1)  # TRNP - пористость
        ]
        
        data.append(row)

    return data



def main():
    base_data = [33913720, 1620.0, 120.0, 0.0415, 3.3395, 93.1]
    aluminium_concentrations = [5,10,15,20,25,30,35,40,45,50,55,60,65]
    dfs = []

    data_water_full = generated_date(base_data)
    df_water_full = pd.DataFrame(data_water_full, columns=['Time', 'NTNC', 'FTNC', 'NTNL', 'FTNL', 'TRNP'])
    df_water_full['Water_height'] = 25 # столбец с высотой воды в см
    df_water_full['Aluminium_Concentration'] = 0 # столбец с концетрацией алюминия в мм

    for concetration in aluminium_concentrations:
        data_aluminium = generated_date(base_data, coef_alumin=concetration)
        df_alum = pd.DataFrame(data_aluminium, columns=['Time', 'NTNC', 'FTNC', 'NTNL', 'FTNL', 'TRNP'])
        df_alum['Aluminium_Concentration'] = concetration
        df_alum['Water_height'] = 25
        dfs.append(df_alum)
        save_dateframe_to_csv(df_alum, 'data_tables', f'df_alum_{concetration}')

    print('df_water_full: \n', df_water_full.head(5))
    for i, concetration in enumerate(aluminium_concentrations):
        print(f'df_aluminium_{concetration}: \n', dfs[i].head(5))

if __name__ == '__main__':
    main()