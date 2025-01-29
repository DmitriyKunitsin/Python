# Ансамблевые методы: Stacking(стекинг). 
# Для выполнения задания возьмите датасет о заболевании сахарным диабетом. 
# В качестве "слабых" учеников используйте ранее изученные методы для классификации . 
# (1) Выполните масштабирование данных. 
# (2) 1-ю конфигурацию сделайте следующую: в качестве слабых учеников возьмите SVM, KNN, 
# метод решающих деревьев с параметрами по умолчанию, в качестве метамодели - логистическую регрессию. 
# (3) 2-ю конфигурацию возьмите с таким же набором слабых учеников, 
# но для каждого задайте наилучшие гиперпараметры на основе выполненных ранее заданий. 
# (4) 3-ю конфигурацию - возьмите по два слабых ученика по каждой модели (одна с гиперпараметрами по умолчанию, вторая - с наилучшими). 
# (5) Для каждого ансамбля моделей выведите его конфигурацию. 
# (6) Проведите сравнение (classification_report) с ранее выполненными работами.
#  Позволило ли существенно улучшить качество прогноза заболевания такое усовершенствование алгоритма? 
# Если есть возможность выполнить подбор гиперпараметров модели - сделайте! 
import pandas as pd
from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler, MinMaxScaler

    

def main():
    data = pd.read_csv('diabetes.csv')
    X = data.drop('Outcome', axis=1)
    y = data['Outcome']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    from sklearn.preprocessing import MinMaxScaler
    # (1) Выполните масштабирование данных. 
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.fit(X_test)


    # (2) Конфигурация 1
    # В качестве слабых учеников возьмите SVM, KNN, 
    # метод решающих деревьев с параметрами по умолчанию, в качестве метамодели - логистическую регрессию. 

    from sklearn.svm import SVC # Классификация
    from sklearn.neighbors import KNeighborsClassifier # Ближайшие соседи
    from sklearn.tree import DecisionTreeClassifier # Деревья решений
    from sklearn.linear_model import LogisticRegression #  Логистическая регрессия
    from sklearn.ensemble import StackingClassifier

    estimators = [("SVM", SVC(probability=True)),
                  ("KNN", KNeighborsClassifier()),
                  ("dt", DecisionTreeClassifier())]
    staking_model_1 = StackingClassifier(estimators=estimators, final_estimator=LogisticRegression())
    # Обучение модели
    staking_model_1.fit(X_train_scaled, y_train)
    # Оценка модели
    y_pred_1 = staking_model_1.predict(X_test_scaled)

    # (3) 2-ю конфигурацию возьмите с таким же набором слабых учеников, 
    # но для каждого задайте наилучшие гиперпараметры на основе выполненных ранее заданий. 

    from sklearn.model_selection import GridSearchCV

    # Гиперпараметры SVM
    svm_param_grid = {
        'C': [0.1,1,10],
        'kernel':['linear','rbf']
    }
    svm_grid = GridSearchCV(SVC(probability=True), svm_param_grid, cv=5)
    svm_grid.fit(X_train_scaled, y_train)

    # Гиперпараметры KNN
    knn_param_grid = {'n_neighbors':[3,5,7]}
    knn_grid = GridSearchCV(KNeighborsClassifier(), knn_param_grid,cv=5)
    knn_grid.fit(X_train_scaled, y_train)

    # Гиператпараметры дерева
    dt_param_grid = {'max_depth':[None,5,10]}
    dt_grid = GridSearchCV(DecisionTreeClassifier(), dt_param_grid, cv=5)
    dt_grid.fit(X_train_scaled, y_train)

    estimators_best = [('SVM', svm_grid.best_estimator_),
                       ('knn', knn_grid.best_estimator_),
                       ('dt', dt_grid.best_estimator_)]

    staking_model_2 = StackingClassifier(estimators=estimators_best, final_estimator=LogisticRegression())
    staking_model_2.fit(X_train_scaled, y_train)
    y_pred_2 = staking_model_2.predict(X_test_scaled)

if __name__ == "__main__":
    main()