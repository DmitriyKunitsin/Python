import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

# 1 Загрузите данные в DataFrame с помощью функции read_csv библиотеки pandas.
df = pd.read_csv("diabetes.csv")

# print(df.head())
# 2 Как наблюдения (объекты) распределились по классам? Сколько
# наблюдений в каждом классе? Для ответа на вопрос используйте метод
# value_counts().
class_counts = df['Outcome'].value_counts()
print(class_counts)

# 3. Разделите данные на признаки и ответы, а затем на обучающую и тестовую выборки.
X = df.drop('Outcome', axis=1)
y = df['Outcome']

X_train, X_test, y_train , y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Обучите линейную SVM-модель с помощью класса SVC из sklearn.svm:
svm = SVC(kernel='linear')
svm.fit(X_train, y_train)

# 5. Оцените качество модели на тестовой выборке. Используйте для этого функцию classification_report. 
y_pred = svm.predict(X_test)
print(classification_report(y_test, y_pred))

#  6. Стандартизируйте данные и постройте модель на стандартизированных
# данных. Используйте для стандартизации класс StandardScaler. Оцените
# качество модели с помощью classification_report. 

scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(X_train)
x_test_scaled = scaler.transform(X_test)

svm_scaled = SVC(kernel='linear')
svm_scaled.fit(x_train_scaled, y_train)

y_pred_scaled = svm_scaled.predict(x_test_scaled)
print(classification_report(y_test, y_pred_scaled))

# 7. Помните ли вы такой способ оценки качества модели как перекрестная
# проверка? Воспользуйтесь перекрестной проверкой, чтобы оценить качество
# моделей. Используйте функцию cross_val_score.

scores = cross_val_score(svm_scaled, X, y, cv=5)
print("Cross-validation scores:", scores)
print("Average cross-validation score:", scores.mean())

# 8. Попробуйте изменить (уменьшить, затем увеличить) значение
# гиперпараметра С. За что он отвечает? Как он влияет на качество модели
# в рассмотренном примере?

# Уменьшение C
svm_low_C = SVC(kernel='linear', C=0.01)
svm_low_C.fit(x_train_scaled, y_train)
y_pred_low_C = svm_low_C.predict(x_test_scaled)
print("Low C classification report:\n", classification_report(y_test, y_pred_low_C))

# Увеличение C
svm_high_C = SVC(kernel='linear', C=100)
svm_high_C.fit(x_train_scaled, y_train)
y_pred_high_C = svm_high_C.predict(x_test_scaled)
print("High C classification report:\n", classification_report(y_test, y_pred_high_C))

# 9. Постройте модель с ядром kernel='rbf'. Как это повлияло на качество
# модели?

svm_rbf = SVC(kernel='rbf')
svm_rbf.fit(x_train_scaled, y_train)

y_pred_rbf = svm_rbf.predict(x_test_scaled)
print("RBF kernel classification report:\n", classification_report(y_test, y_pred_rbf))