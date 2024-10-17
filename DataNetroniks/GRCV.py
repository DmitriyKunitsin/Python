import numpy as np
import pandas as pd
import os
import threading
import queue
import time
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, PoissonRegressor, BayesianRidge
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_squared_error, r2_score



def main():
# Загрузка данных
    folder_path = 'data_tables'
    data_frames = []

    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(folder_path, file))
            data_frames.append(df)
# Объединение всех данных в один
    full_data = pd.concat(data_frames, ignore_index=True) 

    if full_data.isnull().sum().sum() != 0:
        print('Данные не целостные')
        full_data.dropna(inplace=True)
    else:
        print('Данные целостные')

    X = full_data.drop(columns=['Time','TRNP']) # признаки
    y = full_data['TRNP'] # целевое значениеА за
    
    # Разделение данных
    X_train, X_test, y_train , y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Определние модели
    model = BayesianRidge()
    model.fit(X_train, y_train)

    # Шаг 6: Оценка модели
    y_pred = model.predict(X_test)
    score = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    
    print(f'Оценка качества модели с оптимальной степенью полинома: \nR² : {score}\n MAE : {mae}\n MSE: {mse} \n RMSE: {rmse}')

    desired_trnp = 16.5

    NTNC_min = X_train['NTNC'].min()
    NTNC_max = X_train['NTNC'].max()
    FTNC_min = X_train['FTNC'].min()    
    FTNC_max = X_train['FTNC'].max()
    NTNL_min = X_train['NTNL'].min()
    NTNL_max = X_train['NTNL'].max()
    FTNL_min = X_train['FTNL'].min()
    FTNL_max = X_train['FTNL'].max()
    pred_alumin = predict_aluminium_concentration(desired_trnp, model, NTNC_min, NTNC_max, FTNC_min, FTNC_max, NTNL_min, NTNL_max, FTNL_min, FTNL_max)
    print(f"Необходимое содержание алюминия для достижения TRNP {desired_trnp}: {pred_alumin}")
def predict_aluminium_concentration(desired_trnp, model, NTNC_min, NTNC_max, FTNC_min, FTNC_max, NTNL_min, NTNL_max, FTNL_min , FTNL_max):
    aluminum_content_range = np.linspace(0, 150, num=100) # Примерный диапазон содержания алюминия
    results = []
    
    for aluminum_content in aluminum_content_range:
        # Создаем DataFrame с новыми данными
        new_data = pd.DataFrame({
            'NTNC': np.random.uniform(NTNC_min, NTNC_max), 
            'FTNC': np.random.uniform(FTNC_min, FTNC_max),  
            'NTNL': np.random.uniform(NTNL_min, NTNL_max),        
            'FTNL': np.random.uniform(FTNL_min, FTNL_max),       
            'Aluminium_Concentration': [aluminum_content],
            'Water_height': [25]                      
        })

        predicted_trnp = model.predict(new_data)

        results.append((aluminum_content, predicted_trnp[0]))

    # Преобразуем результаты в DataFrame для удобства анализа
    results_df = pd.DataFrame(results, columns=['Aluminium', 'Predicted_TRNP'])
    # Находим содержание алюминия для нужного TRNP
    closest_value = results_df.iloc[(results_df['Predicted_TRNP'] - desired_trnp).abs().argsort()[:1]]
    return closest_value['Aluminium'].values[0]
    
if __name__ == '__main__':
    main()