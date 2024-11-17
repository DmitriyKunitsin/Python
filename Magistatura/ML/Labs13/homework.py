'''
Классификация: кодирование категориальных признаков (например, One Hot Encoding), 
скалирование признаков (нормализация и стандартизация),
подбор гиперпараметров моделей (GridSearchCV).
Задание: 
(1) загрузите данные о доходах населения. 
(2) уберите строки с неизвестными значениями. 
(3) постройте тепловую матрицу корреляции. Если обнаружатся полностью зависимые признаки - оставьте только один из двух. 
(4) рассмотрев данные, определите порядковые категориальные признаки (если они есть на Ваш взгляд) и вручную перекодируйте их в числовые. 
Остальные категориальные признаки закодируйте методом One Hot Encoding или pd.get_dummies. 
(5) разбейте выборку на обучающую и тестовую, обучите модель логистической регрессии, оцените качество с помощью classification_report. 
(6) выполните нормализацию (normalizer) признаков и повторите пункт 5. 
(7) выполните стандартизацию (standartscaller) признаков и повторите пункт 5. 
(8) выполните масштабирование minmaxscaller и повторите пункт 5. 
(9) Сравнив 5, 6, 7, 8 ответьте на вопрос: как меняется качество модели? 
(10) Постройте гистограммы распределения для какого-нибудь столбца (например, fnlwgt) 
без масштабирования и с различными рассмотренными способами масштабирования. 
(11) Подберите с помощью GridSearchCV оптимальное значение гиперпараметра С (L2-регуляризация) модели логистической регрессии. 
(12) сделайте выводы по проделанной работе.
'''

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler, MinMaxScaler, Normalizer


def main():
    '''(1) загрузите данные о доходах населения. '''
    data = pd.read_csv('adult.csv')
    
    '''(2) замените строки с '?' на NaN и уберите строки с неизвестными значениями. '''
    data.replace('?', np.nan, inplace=True)
    data_cleaned = data.dropna()
    
    '''(3) постройте тепловую матрицу корреляции. Если обнаружатся полностью зависимые признаки - оставьте только один из двух. '''
    numeric_data = data_cleaned.select_dtypes(include=[np.number])

    correlation_matrix = numeric_data.corr()

    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True)
    plt.title('Тепловая матрица корреляции')
    plt.show()

    correlated_features = set()
    for i in range(len(correlation_matrix.columns)):
        for j in range(i):
            if abs(correlation_matrix.iloc[i, j]) == 1:
                colname = correlation_matrix.columns[i]
                correlated_features.add(colname)

    for feature in correlated_features:
        if feature in data_cleaned.columns:
            data_cleaned = data_cleaned.drop(columns=[feature])
            break  

    print("Удаленные полностью зависимые признаки:", correlated_features)

    '''(4) рассмотрев данные, определите порядковые категориальные признаки (если они есть на Ваш взгляд) и вручную перекодируйте их в числовые. 
        Остальные категориальные признаки закодируйте методом One Hot Encoding или pd.get_dummies. '''
    label_mapping = {label: idx for idx, label in enumerate(data_cleaned['marital.status'].unique())}
    data_cleaned['marital.status_encoded'] = data_cleaned['marital.status'].apply(lambda x: label_mapping[x])

    print(data_cleaned[['marital.status_encoded', 'marital.status']].head)

    category_columns = ['occupation','workclass', 'relationship', 'race', 'sex', 'native.country']
    df_encoded = pd.get_dummies(data_cleaned, columns=category_columns, drop_first=True)

    print(df_encoded.info())

    '''(5) разбейте выборку на обучающую и тестовую, обучите модель логистической регрессии, оцените качество с помощью classification_report. '''
    X = df_encoded.drop(columns=['income', 'education', 'marital.status', 'marital.status_encoded'])
    y = df_encoded['income'].apply(lambda x: 1 if x == '>50K' else 0)  

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    '''(6) выполните нормализацию (normalizer) признаков и повторите пункт 5. '''
    # Нормализация признаков
    normalizer = Normalizer()
    X_train_normalized = normalizer.fit_transform(X_train)
    X_test_normalized = normalizer.transform(X_test)

    # Обучение модели логистической регрессии на нормализованных данных
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_normalized, y_train)

    # Предсказание и оценка качества модели
    y_pred = model.predict(X_test_normalized)
    print(classification_report(y_test, y_pred))

    '''(7) выполните стандартизацию (standartscaller) признаков и повторите пункт 5. '''
    # Стандартизация признаков
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Обучение модели логистической регрессии на стандартизированных данных
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train)

    # Предсказание и оценка качества модели на стандартизированных данных
    y_pred = model.predict(X_test_scaled)
    print("Classification report with standardization:")
    print(classification_report(y_test, y_pred))

    '''(8) выполните масштабирование minmaxscaller и повторите пункт 5. '''
    # Масштабирование признаков с помощью MinMaxScaler
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Обучение модели логистической регрессии на масштабированных данных
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train)

    # Предсказание и оценка качества модели на масштабированных данных
    y_pred = model.predict(X_test_scaled)
    print("Classification report with MinMax scaling:")
    print(classification_report(y_test, y_pred))

    '''(9) Сравнив 5, 6, 7, 8 ответьте на вопрос: как меняется качество модели? '''
    '''
    1. Точность (Accuracy): Около 84% для трех из четырех предобработок, что говорит о хорошей общей производительности модели.

    2. Precision (точность): Для класса 1 точность выше при стандартизации (92%), но ниже при MinMaxScaler (71%).

    3. Recall (полнота): Полнота для класса 1 значительно улучшилась с MinMaxScaler (59%) по сравнению со стандартизацией (9%).

    4. F1-score: F1-score для класса 1 также лучше с MinMaxScaler (64%) против 17% при стандартизации.

    5. Вывод: Если важнее минимизировать ложные отрицательные срабатывания для класса 1, лучше использовать MinMaxScaler. 
    '''

    '''(10) Постройте гистограммы распределения для какого-нибудь столбца (например, fnlwgt) 
    без масштабирования и с различными рассмотренными способами масштабирования. '''

    fnlwgt = df_encoded['fnlwgt']

    standard_scaler = StandardScaler()
    fnlwgt_standard_scaled = standard_scaler.fit_transform(fnlwgt.values.reshape(-1, 1))

    minmax_scaler = MinMaxScaler()
    fnlwgt_minmax_scaled = minmax_scaler.fit_transform(fnlwgt.values.reshape(-1, 1))

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.hist('fnlwgt', bins=30, color='blue', alpha=0.7)
    plt.title('Гистограмма без масштабирования')
    plt.xlabel('fnlwgt')
    plt.ylabel('Frequency')

    plt.subplot(1, 3, 2)
    plt.hist(fnlwgt_standard_scaled, bins=30, color='orange', alpha=0.7)
    plt.title('Гистограмма с помощью StandardScaler')
    plt.xlabel('Standard Scaled fnlwgt')
    plt.ylabel('Frequency')

    plt.subplot(1, 3, 3)
    plt.hist(fnlwgt_minmax_scaled, bins=30, color='green', alpha=0.7)
    plt.title('Гистограмма с помощью MinMaxScaler')
    plt.xlabel('MinMax Scaled fnlwgt')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.show()

    '''(11) Подберите с помощью GridSearchCV оптимальное значение гиперпараметра С (L2-регуляризация) модели логистической регрессии. '''

    # Определите параметры для GridSearchCV
    param_grid = {
        'C': np.logspace(-4, 4, 20)  # Параметры C от 0.0001 до 10000
    }
    
    # Создайте объект GridSearchCV
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy')
    
    # Обучите модель с использованием GridSearchCV
    grid_search.fit(X_train, y_train)
    
    # Выведите лучшие параметры и результаты
    print("Лучшее значение C:", grid_search.best_params_['C'])
    print("Лучшая точность на валидационной выборке:", grid_search.best_score_)

if __name__ == "__main__":
    main()
