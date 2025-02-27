# В прилагаемом примере приводится код для загрузки датасета, 
# содержащего изображения рукописных цифр. 
# (1) Загрузите датасет NMIST. 
# (2) Получите информацию о количестве изображений для обучения и тестирования. 
# (3) Отобразите несколько изображений. 
# (4) Подготовьте данные для обучения моделей классификации. 
# (5) Создайте модели SVM, KNN, метод решающих деревьев, логистическую регрессию для классификации изображений. 
# (6) оцените качество созданных моделей (classification_report). На каких цифрах наблюдаются сложности их детекции? 
# (7) Подготовьте свои картинки (например, в Paint), при этом изображение сделайте близким к квадратному и размер задайте небольшой, 
# в то же время толщина кисти, которой Вы будете писать цифры, должна быть существенной. 
# Сравните эффективность работы созданных классификаторов. 
# (8) Используя метод главных компонент (PCA), осуществите понижение размерности данных. 
# Визуализируйте данные в проекции на первые две главные компоненты. 
# (9) Выполните понижение размерности методом t-SNE, отобразите результат. 

from keras._tf_keras.keras.datasets import mnist
from keras._tf_keras.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

def main():
    # список с названиями классов
    classes = ['ноль', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять']
    # (1) Загрузите датасет NMIST. 
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    # (2) Получите информацию о количестве изображений для обучения и тестирования.
    print('Размер коллекции для обучения: ',x_train.shape)
    print('Размер коллекции для тестирования: ',x_test.shape)

    # (3) Отобразите несколько изображений.
    plt.figure()
    for i in range(50):
        plt.subplot(5,10,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(x_train[i], cmap=plt.cm.binary)
        plt.xlabel(classes[y_train[i]])
    plt.show()


    # (4) Подготовьте данные для обучения моделей классификации. 
    # для использования необходимо преобразовать данные о пикселях картинки из 2D в 1D
    # 28 x 28 = 784
    x_train = x_train.reshape(60000,784)
    x_test = x_test.reshape(10000, 784)
    #Значение интенсивности пикселей в изображении находится в интервале [0,255].
    #Для наших целей их необходимо нормализовать - привести к значениям в интервале [0,1].
    x_train = x_train /255
    x_test = x_test / 255
    #Посмотрим, как выглядит ответ
    print(y_train[0])
    print(type(y_train[0]))

 
    # # (5) Создайте модели SVM, KNN, метод решающих деревьев, логистическую регрессию для классификации изображений. 
    models = {
        "SVM" : svm.SVC(gamma='scale'),
        "KNN" : KNeighborsClassifier(n_neighbors=3),
        "DT" : DecisionTreeClassifier(),
        "LOGIC REGRESSION" : LogisticRegression(max_iter= 1000)
    }

    # # (6) оцените качество созданных моделей (classification_report). На каких цифрах наблюдаются сложности их детекции? 
    for model_name, model in models.items():
        model.fit(x_train, y_train)

        y_pred = model.predict(x_test)

        accuracy = accuracy_score(y_test, y_pred)
        
        print(f'Точность модели {model_name}: {accuracy:.4f}')
        print(classification_report(y_test, y_pred))
    # # (7) Подготовьте свои картинки (например, в Paint), при этом изображение сделайте близким к квадратному и размер задайте небольшой, 
    # # в то же время толщина кисти, которой Вы будете писать цифры, должна быть существенной. 
    custom_images = Get_list_and_load_image()
    for i in range(0,10):
        image = custom_images[i]
        plt.imshow(image.convert('RGBA'))
        plt.show()

    # (8) Используя метод главных компонент (PCA), осуществите понижение размерности данных. 
    # Визуализируйте данные в проекции на первые две главные компоненты. 

    from sklearn.decomposition import PCA

    pca = PCA(n_components=2)
    x_pca = pca.fit_transform(x_train)

    # Визуализация данных в проекции на первые две главные компоненты.
    plt.figure(figsize=(8, 6))
    plt.scatter(x_pca[:, 0], x_pca[:, 1], c=y_train, cmap='viridis', edgecolor='none', alpha=0.5, s=20)
    plt.title('PCA: Проекция на первые две главные компоненты')
    plt.xlabel('Первая главная компонента')
    plt.ylabel('Вторая главная компонента')
    plt.colorbar()
    plt.show()

    # (9) Выполните понижение размерности методом t-SNE, отобразите результат. 
    


def Get_list_and_load_image():
    CustomImage = []
    for i in range(0,10):
        prefix_name_image = "resize_"
        postfix_name_image = ".png"
        path = f"C:\\Users\\d.kunicin\\Python\\Python\\Magistatura\\ML\\Semester_2\\Lab_0_5\\myNumbers\\{prefix_name_image}{i}{postfix_name_image}"
        images = image.load_img(path, target_size=(28,28), color_mode="grayscale")
        CustomImage.append(images)
        print(f'Изображение {prefix_name_image} {i} {postfix_name_image} загружено')
    return CustomImage

if __name__ == '__main__':
    main()