# В приложении к заданию приведены данные о пациентах. 
# На основе Вашего опыта предлагаю провести предварительную обработку данных, 
# построить модель бинарной классификации (болен, здоров), 
# определить качество построенной модели. 
# Для отдельных групп данных или для изначального датасета провести кластерный анализ. 
# Удачи! 

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder 
from sklearn.metrics import confusion_matrix
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def main():
    # Предварительная обработка данных
    data = pd.read_excel('ATEROSKLEROZ++10.02.23.xls', engine='xlrd')

    print(data.isnull().sum())
    # Удаляю только те столбцы, где более 50% данных Nan
    threshold = 0.5 * len(data)
    data.dropna(inplace=True, thresh=threshold, axis=1)
    data.drop_duplicates(inplace=True)
    print(data.isnull().sum())

    # Кастую в int
    le = LabelEncoder()
    encode_columns = [ 'Болен/Здоров','Курение' , "Национальность", 'Возраст (на момент операции)',"Пол",
                      "PPARG rs1801282", "FABP2rs1799883", "ADRB3rs4994", "FTOrs9939609",
                       "GSTP114", "GSTP105", "TP53", "CAT", "MTR", "MTHFR", "MnSOD", "GPx1" ]
    for i in encode_columns:
        data[i] = le.fit_transform(data[i])

    # Заполняю оставшиеся пустые места, средним
    data.fillna(data.mean(), inplace=True)
    
    X = data.drop('Болен/Здоров',axis=1)
    y = data['Болен/Здоров']

    from sklearn.model_selection import train_test_split
    
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.25, random_state=42)

    from sklearn.preprocessing import StandardScaler

    # Нормализация данных
    ss_train = StandardScaler()
    X_train = ss_train.fit_transform(X_train)
    X_test = ss_train.transform(X_test)

    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.svm import SVC
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.ensemble import StackingClassifier
    from sklearn.linear_model import LogisticRegression

    estim_clasiffer = [
        ("SVC", SVC()),
        ("Gradient" , GradientBoostingClassifier(n_estimators=100)),
        ("Forest", RandomForestClassifier())
    ]

    stack_model = StackingClassifier(estimators=estim_clasiffer, final_estimator=LogisticRegression())
    stack_model.fit(X_train, y_train)
    y_pred = stack_model.predict(X_test)
        
    from sklearn.metrics import classification_report
    print("\nClassification Report для конфигурации :")
    print(classification_report(y_test, y_pred)) 
    # Либо свершилось чудо, либо где-то ошибка, то получился идеальный результат
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Class 0', 'Class 1'], yticklabels=['Class 0', 'Class 1'])
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title('Confusion Matrix')
    plt.show()

    plot_elbow_method(X)

    n_clusters = 3
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    data['Cluster'] = kmeans.fit_predict(X)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    plt.figure(figsize=(10, 6))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=data['Cluster'], cmap='viridis', marker='o')
    plt.title('Кластеры пациентов')
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')
    plt.colorbar(label='Кластер')
    plt.show()


def plot_elbow_method(X):
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, random_state=42)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), wcss)
    plt.title('Метод локтя')
    plt.xlabel('Количество кластеров')
    plt.ylabel('WCSS')
    plt.show()



if __name__ == '__main__':
    main()
