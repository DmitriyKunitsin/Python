from sklearn.pipeline import Pipeline

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LassoCV, RidgeCV, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import classification_report, confusion_matrix


def main():
    # 1 Загрузил данные из файла
    df = pd.read_csv("logistic.csv")
    df.columns = ["target", "feature_1", "feature_2"]
    print(df.head())

    # 2 Как наблюдения распределились по классам?
    print(df["target"].value_counts())

    # 3 Отобразите точками на плоскости признаки, различая классы цветом.
    plt.figure(figsize=(10,6))

    class_0 = df[df["target"] == -1]
    class_1 = df[df["target"] == 1]

    plt.scatter(class_0["feature_1"], class_0["feature_2"], color='blue', label="Class 0", alpha=0.5)
    plt.scatter(class_1["feature_1"], class_1["feature_2"], color='red', label="Class 1", alpha=0.5)
    
    plt.title("Распределение классов по признакам")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.legend()
    plt.grid()
    plt.show()

    # 4 Разделите данные на признаки и ответы. 
    X = df[["feature_1", "feature_2"]] # признаки
    y = df["target"]                   # ответы

    # 5 Обучите модель логистической регрессии (LogisticRegression или LogisticRegression_CV, 
    # дайте описание гиперпараметров модели). 
    # Для обучения используйте всю выборку. 
    model = LogisticRegression()
    model.fit(X,y)

    y_pred = model.predict(X)

    # Оценка модели
    print("Матрица путаницы:")
    print(confusion_matrix(y, y_pred))
    
    print("nОтчет о классификации:")
    print(classification_report(y, y_pred))

if __name__ == "__main__":
    main()