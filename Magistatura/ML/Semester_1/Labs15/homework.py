import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score

# 1. Загрузка необходимых библиотек и данных
# Загрузка данных
df = pd.read_csv('diabetes.csv')

# 2. Подготовка данных
# Разделение данных на признаки и целевую переменную
X = df.drop('Outcome', axis=1)  
y = df['Outcome']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Стандартизация данных
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 3. Определение оптимального количества соседей для KNN
accuracies = []
k_values = range(1, 21)  # Проверим значения K от 1 до 20

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_scaled, y_train)
    y_pred = knn.predict(X_test_scaled)
    accuracies.append(accuracy_score(y_test, y_pred))

# Построение графика зависимости точности от количества соседей
plt.figure(figsize=(10, 6))
plt.plot(k_values, accuracies, marker='o')
plt.title('Зависимость точности модели KNN от количества соседей')
plt.xlabel('Количество соседей (K)')
plt.ylabel('Точность')
plt.xticks(k_values)
plt.grid()
plt.show()

# 4. Определение оптимального K и оценка модели KNN

optimal_k = k_values[np.argmax(accuracies)]
print(f'Оптимальное количество соседей: {optimal_k}')

# Обучение модели с оптимальным K
knn_optimal = KNeighborsClassifier(n_neighbors=optimal_k)
knn_optimal.fit(X_train_scaled, y_train)
y_pred_knn = knn_optimal.predict(X_test_scaled)

# Оценка модели KNN
print("Classification report для KNN:")
print(classification_report(y_test, y_pred_knn))

# 5. Оценка модели SVM для сравнения
# Обучение модели SVM
svm = SVC(kernel='linear')
svm.fit(X_train_scaled, y_train)
y_pred_svm = svm.predict(X_test_scaled)

# Оценка модели SVM
print("Classification report для SVM:")
print(classification_report(y_test, y_pred_svm))
