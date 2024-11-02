from sklearn.pipeline import Pipeline

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LassoCV, RidgeCV, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


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
    model = LogisticRegression(penalty="l1", solver="liblinear", max_iter=1000)
    # Тип регуляризации, используемой в модели. Возможные значения: 'l1': Lasso регуляризация (устраняет некоторые коэффициенты, делая их равными нулю).
    # Алгоритм, используемый для оптимизации. Возможные значения:'liblinear': Подходит для небольших наборов данных и поддерживает L1 регуляризацию.
    # Максимальное количество итераций для алгоритма оптимизации. По умолчанию 100. Увеличение этого значения может помочь при сходимости модели.

    model.fit(X,y)

    y_pred = model.predict(X)
    y_pred_proba = model.predict_proba(X)[:, 1]

    # 6 Отобразите на ранее полученном рисунке гиперплоскость, получив необходимые коэффициенты из построенной модели. 
    coef = model.coef_[0]
    intercept = model.intercept_[0]

    x_values = np.linspace(X["feature_1"].min(), X["feature_1"].max(), 100)
    y_values = -(coef[0] * x_values + intercept) / coef[1]
    
    plt.scatter(class_0["feature_1"], class_0["feature_2"], color='blue', label="Class 0", alpha=0.5)
    plt.scatter(class_1["feature_1"], class_1["feature_2"], color='red', label="Class 1", alpha=0.5)
    plt.plot(x_values, y_values, color='green', label='Decision Boundary')

    plt.title("Распределение классов по признакам с гиперплоскостью")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.legend()
    plt.grid()
    plt.show()

    # 7 получите матрицу несоответствий / ошибок (confusion matrix). Дайте пояснения. 
    cm = confusion_matrix(y, y_pred)
    print("Матрица несоответствий:n", cm)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    disp.plot(cmap=plt.cm.Blues)
    plt.title("Матрица несоответствий")
    plt.show()
    #
    # [TN , FP]
    # [FN , TP]
    #  TN (True Negative): Количество объектов, правильно классифицированных как класс 0.
    #  FP (False Positive): Количество объектов, неправильно классифицированных как класс 1 (на самом деле класс 0).
    #  FN (False Negative): Количество объектов, неправильно классифицированных как класс 0 (на самом деле класс 1).
    #  TP (True Positive): Количество объектов, правильно классифицированных как класс 1.
    # Чем больше значения TN и TP, тем лучше модель.
    # Чем меньше значения FP и FN, тем лучше модель.

    # 8 Получите оценки качества классификации (на обучающей выборке): доля правильных ответов, точность, полнота, F-меру, AUC. Дайте пояснения. 
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, pos_label=1)
    recall = recall_score(y, y_pred, pos_label=1)
    f1 = f1_score(y, y_pred, pos_label=1)
    auc = roc_auc_score(y, y_pred_proba)

    print(f"Доля правильных ответов (Accuracy): {accuracy:.2f}")
    # Доля правильных ответов (Accuracy): Это доля правильно классифицированных объектов от общего числа объектов. Вычисляется как (TP + TN) / (TP + TN + FP + FN).
    print(f"Точность (Precision): {precision:.2f}")
    # Точность (Precision): Это доля истинных положительных результатов от всех положительных результатов. Вычисляется как TP / (TP + FP). Высокая точность означает, что модель делает мало ложноположительных ошибок.
    print(f"Полнота (Recall): {recall:.2f}")
    # Полнота (Recall): Это доля истинных положительных результатов от всех фактических положительных объектов. Вычисляется как TP / (TP + FN). Высокая полнота означает, что модель делает мало ложноотрицательных ошибок.
    print(f"F-мера (F1 Score): {f1:.2f}")
    #  F-мера (F1 Score): Это гармоническое среднее между точностью и полнотой. Вычисляется как 2 × (Precision × Recall) / (Precision + Recall). F-мера полезна, когда необходимо учитывать как ложноположительные, так и ложноотрицательные ошибки.
    print(f"AUC: {auc:.2f}")
    # AUC (Area Under the Curve): Это площадь под кривой ROC (Receiver Operating Characteristic). AUC показывает способность модели различать классы. Значение AUC варьируется от 0 до 1; чем ближе к 1, тем лучше модель.


    # 9 В окрестности гиперплоскости задайте некоторое количество случайных точек (отобразите их на рисунке новым цветом). Определите при помощи построенной модели принадлежность классу.
    num_random_points = 10
    random_points = np.random.uniform(low=[X["feature_1"].min(), X["feature_2"].min()],
                                       high=[X["feature_1"].max(), X["feature_2"].max()],
                                       size=(num_random_points, 2))

    # Определение принадлежности классу
    random_predictions = model.predict(random_points)

    # Отображение случайных точек на графике
    for point, prediction in zip(random_points, random_predictions):
        if prediction == -1:
            plt.scatter(point[0], point[1], color='orange', label="Случайная точка (Class -1)", alpha=0.7)
        else:
            plt.scatter(point[0], point[1], color='purple', label="Случайная точка (Class 1)", alpha=0.7)

    plt.title("Случайные точки и их предсказанные классы")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()