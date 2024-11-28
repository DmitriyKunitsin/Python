'''
Метод решающих деревьев: задание и необходимые материалы приложены в файлах. 
В 5м пункте дополнительно: отобразите на плоскости распределение наблюдений, взяв 2а наиболее значимых признака. 
Для ответа на вопрос в 10м пункте попробуйте уровнять количество наблюдений по классам (RandomUnderSampler, RandomOverSampler).
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier, plot_tree
# from imblearn.over_sampling import RandomOverSampler
# from imblearn.under_sampling import RandomUnderSampler
def load_data(file_path):
    return pd.read_csv(file_path) 

def visualize_tree(model, feature_names):
    plt.figure(figsize=(10, 5))
    plot_tree(model, filled=True, feature_names=feature_names, class_names=['No Diabetes', 'Diabetes'], rounded=True)
    plt.title('Дерево решений (глубина = 2)')
    plt.show()

def main():
    # 1 Загрузите данные в DataFrame с помощью функции read_csvбиблиотекиpandas.
    data = load_data('diabetes.csv')
    
    # 2 Разделите данные на обучающую и тестовую выборкис помощью функцииtrain_test_split.
    X = data.drop('Outcome', axis=1)
    y = data['Outcome']

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)

    # 3 Постройте дерево решений с помощьюклассаDecisionTreeClassifier с гиперпараметрами по умолчанию

    model = DecisionTreeClassifier(max_depth=2)
    model.fit(X_train, y_train)

    # 4 Отобразите дерево решений с глубиной 2. Опишите процесс принятия решения
    visualize_tree(model, X.columns)

    # 5 Получите информативность признаков. Какие признаки наиболее значимые, какие - наименее?

    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]

    plt.figure(figsize=(10, 6))
    plt.title("Важность признаков")
    plt.bar(range(X.shape[1]), importances[indices], align="center")
    plt.xticks(range(X.shape[1]), X.columns[indices], rotation=90)
    plt.xlim([-1, X.shape[1]])
    plt.show()
    # Признаки ближе к 1, являются наиболее значимыми для модели

    # 6 Оцените качествомодели с помощьюфункцииclassification_report

    y_pred = model.predict(X_test)

    report = classification_report(y_test, y_pred)
    print(report)

    # 8 Подберите оптимальное значение гиперпараметра max_depthс помощьюпоиска посетке(класс GridSearchCV).
    param_grid = {
        'max_depth': np.arange(1,11)
    }

    grid_seatch = GridSearchCV(model, param_grid , cv=5, scoring='accuracy')

    grid_seatch.fit(X_train,y_train)

    print('Лучшие параметры : ', grid_seatch.best_params_)
    print('Лучшая точность : ', grid_seatch.best_score_)

    best_model = grid_seatch.best_estimator_
    y_pred = best_model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # 9 Обучите модель с оптимальным max_depthи оцените результат.

    optimal_model = DecisionTreeClassifier(max_depth=3)
    optimal_model.fit(X_train, y_train)

    y_opti_pred = optimal_model.predict(X_test)

    print(classification_report(y_test, y_opti_pred))
    

    
if __name__ == '__main__':
    main()