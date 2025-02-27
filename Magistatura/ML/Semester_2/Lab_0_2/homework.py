# Ансамблевые методы: Bagging (беггинг). 
# Для выполнения задания возьмите датасет о заболевании сахарным диабетом. 
# (1) Выполните масштабирование данных. 
# (2) Для построения ансамбля в качестве базового метода используйте поочередно изученные ранее методы с наилучшими гиперпараметрами. 
# (3) Получите структуру построенной модели. 
# (4) Возьмите за основу один из базовых алгоритмов и определите оптимальное количество базовых алгоритмов в ансамбле (GridSearchCV). 
# Сделайте выводы! 
import pandas as pd
from sklearn.model_selection import train_test_split
def main():
    data = pd.read_csv('diabetes.csv')
    X = data.drop('Outcome', axis=1)
    y = data['Outcome']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    from sklearn.preprocessing import MinMaxScaler
    # (1) Выполните масштабирование данных. 
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # (2) Для построения ансамбля в качестве базового метода используйте поочередно изученные ранее методы с наилучшими гиперпараметрами. 
    from sklearn.svm import SVC # Классификация
    from sklearn.model_selection import GridSearchCV    
    # Гиперпараметры SVM
    svm_param_grid = {
        'C': [0.1,1,10],
        'kernel':['linear','rbf']
    }
    svm_grid = GridSearchCV(SVC(probability=True), svm_param_grid, cv=5)
    svm_grid.fit(X_train_scaled, y_train)
    from sklearn.ensemble import BaggingClassifier
    bagging_model = BaggingClassifier(estimator=svm_grid.best_estimator_)
    param_grid = {
        'n_estimators': [10,20,30,50,100]
    }
    grid_search = GridSearchCV(estimator=bagging_model, param_grid=param_grid, cv=5)
    grid_search.fit(X_train_scaled, y_train)
    # (3) Получите структуру построенной модели.
    print('Лучшие параметры на GridSearchCV')
    print(grid_search.best_params_)

    best_bagging_model = grid_search.best_estimator_
    y_pred = best_bagging_model.predict(X_test_scaled)
    from sklearn.metrics import accuracy_score, classification_report
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Лучший Accuracy c n_estimators = {accuracy:.4f}')
    print(classification_report(y_test, y_pred))

if __name__ == '__main__':
    main()
