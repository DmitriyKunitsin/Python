# Ансамблевые методы: частный случай Bagging - метод случайного леса (Random Forest).
# Для выполнения задания возьмите датасет о заболевании сахарным диабетом. 
# В качестве базового метода используйте ранее изученный метод решающих деревьев. 
# Обязательно дайте описание гиперпараметров построенной модели. 
# Позволило ли существенно улучшить качество прогноза заболевания такое усовершенствование алгоритма? 
# Определите оптимальное количество базовых алгоритмов в ансамбле 
# (постройте график зависимости точности определения класса от количества деревьев). 
# Определите оптимальную глубину деревьев. 

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
def main():
    data = pd.read_csv('diabetes.csv')
    X = data.drop('Outcome', axis=1)
    y = data['Outcome']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    param_grid_rf  = {
        'n_estimators' : [10,50,100,200],
        'max_depth':[None,5,10,15,20]
    }
    rf_model = RandomForestClassifier(random_state=42)
    grid_search_rf = GridSearchCV(estimator=rf_model, param_grid=param_grid_rf, cv=5)
    grid_search_rf.fit(X_train, y_train)
    print(f'Лучшие параметры для Ranom FOrest')
    print(grid_search_rf.best_estimator_)
    best_rf_model = grid_search_rf.best_estimator_
    y_pred_rf = best_rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred_rf)
    print(f"Accuracy адаптивного бустинга : {accuracy:.4f}")


    n_estim_range = [10,50,100,200]
    accuracies = []
    for n in n_estim_range:
        tmp_model = RandomForestClassifier(n_estimators=n, random_state=42)
        tmp_model.fit(X_train, y_train)
        tmp_y_pred = tmp_model.predict(X_test)
        accuracies.append(accuracy_score(y_test, tmp_y_pred))
    plt.plot(n_estim_range,accuracies, marker='o')
    plt.title('Зависимость точности от колличества деревьев')
    plt.xlabel('Колличество деревьев (n_estimators)')
    plt.ylabel('Точность')
    plt.xticks(n_estim_range)
    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()