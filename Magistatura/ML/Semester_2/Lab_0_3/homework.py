# Ансамблевые методы: Boosting (бустинг). 
# Для выполнения задания возьмите датасет о заболевании сахарным диабетом. 
# Перечень заданий аналогичен предыдущим ансамблевым работам, 
# однако обязательно постройте модель, реализующую адаптивный бустинг, 
# и модель, реализующую градиентный бустинг! 

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
def main():
    data = pd.read_csv('diabetes.csv')
    X = data.drop('Outcome', axis=1)
    y = data['Outcome']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Модель адаптивноо бустингга
    ada_param_grid = {
        'n_estimators' : [50,100,150,200]
    }
    ada_model = AdaBoostClassifier(random_state=42)
    ada_grid_search = GridSearchCV(estimator=ada_model,  param_grid=ada_param_grid, cv=5)
    ada_grid_search.fit(X_train, y_train)
    print(f'Лучшие параметры для AdaBoost ')
    print(ada_grid_search.best_estimator_)
    best_ada_model = ada_grid_search.best_estimator_
    y_pred_ada = best_ada_model.predict(X_test)
    accuracy_ada = accuracy_score(y_test, y_pred_ada)
    print(f"Accuracy адаптивного бустинга : {accuracy_ada:.4f}")
    print(classification_report(y_test, y_pred_ada))


    gb_param_grid = {
        'n_estimators' : [50,100,150,200]
    }
    gb_model = GradientBoostingClassifier(random_state=42)
    gb_grid_search = GridSearchCV(estimator=gb_model, param_grid=gb_param_grid, cv=5)
    gb_grid_search.fit(X_train, y_train)
    print(f'Лучшие параметры для GradientBoost ')
    print(gb_grid_search.best_estimator_)
    best_gb_model = gb_grid_search.best_estimator_
    y_pred_gb = best_gb_model.predict(X_test)

    accuracy_gb = accuracy_score(y_test, y_pred_gb)
    print(f"Accuracy адаптивного бустинга : {accuracy_gb:.4f}")
    print(classification_report(y_test, y_pred_gb))



if __name__ == '__main__':
    main()