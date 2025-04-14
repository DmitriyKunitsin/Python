"""
    Распознавание лиц на фото и видео. Изучите прилагаемый блокнот. 
    1) Возьмите несколько фотографий (групповых, в разном ракурсе, попробуйте добавить животных и т.д.). 
    Определите лица на фото, выделив их прямоугольной рамкой, 
    при помощи библиотеки Open CV, face_recognition из dlib, MTCNN (дополнительно отметьте характерные признаки лиц точками). 
    Сравните полученные результаты. 
    2) Подгрузите видео и образцы фото 3-х человек, которых надо найти на видео. 
    Используя библиотеку face_recognition, получите ответ - кто из искомых личностей присутствует на видео. 

"""
import numpy as np 
import os
import matplotlib.pyplot as plt


def main():


    photos = list(filter(lambda x : '.png' in x, os.listdir()))
    print(f'Список всех фоток : {photos}') 

    "Детекция лиц в Open CV"
    # for photo in photos:
    #     face_det_cv2(photo)

    "Детекция лиц в Face recording"
    # for photo in photos:
    #     face_det_fr(photo)
    

"""
    https://habr.com/ru/articles/519454/
    Доп инфу черпал от сюда
"""

"""
Функция detectMultiScale принимает 4 параметра:

    1) Обрабатываемое изображение в градации серого.
    2) Параметр scaleFactor. Некоторые лица могут быть больше других, поскольку находятся ближе, 
        чем остальные. Этот параметр компенсирует перспективу.
    3) Алгоритм распознавания использует скользящее окно во время распознавания объектов. 
        Параметр minNeighbors определяет количество объектов вокруг лица. 
        То есть чем больше значение этого параметра, тем больше аналогичных объектов необходимо алгоритму, 
        чтобы он определил текущий объект, как лицо. Слишком маленькое значение увеличит количество ложных срабатываний, 
        а слишком большое сделает алгоритм более требовательным.
    4) minSize — непосредственно размер этих областей.

"""
def face_det_cv2(photo_name):
    import cv2
    """
        Чтобы считать изображение в RGB — cv2.IMREAD_COLOR, в оттенках серого — cv2.IMREAD_GRAYSCALE.
    """
    img_color = cv2.imread(photo_name)
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


    faces = face_cascade.detectMultiScale(
        img_gray,
        scaleFactor = 1.05, # Данный параметр компенсирует перспективу ( ближе дальше лица относительно друг друга ) 
        minNeighbors= 12, # Уменьшение этого значения может помочь обнаружить больше лиц, но также увеличивает количество ложных срабатываний
        minSize=(35,35) # Этот параметр определяет минимальный размер лиц, которые будут обнаружены. 
    )

    check_len_face = len(faces)

    for(x,y,w,h) in faces:
        cv2.rectangle(img_color, (x,y), (x+w, y+h), (255,255,0), 2)

    face_profile_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

    faces = face_profile_cascade.detectMultiScale(
        img_gray,
        scaleFactor = 1.05, # Данный параметр компенсирует перспективу ( ближе дальше лица относительно друг друга ) 
        minNeighbors= 12, # Уменьшение этого значения может помочь обнаружить больше лиц, но также увеличивает количество ложных срабатываний
        minSize=(65,65) # Этот параметр определяет минимальный размер лиц, которые будут обнаружены. 
    )

    # Отрисовка прямугольков вокруг лиц
    for(x,y,w,h) in faces:
        cv2.rectangle(img_color, (x,y), (x+w, y+h), (255,255,0), 2)
    
    faces_detected = "Лиц обнаружено :" + format(len(faces) + check_len_face)
    print(faces_detected)
    
    plt.figure(figsize=(8,8), dpi=90)
    plt.imshow(cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB))
    plt.show()
    cv2.waitKey(0)

"Детекция лиц на основе Face Recording"
def face_det_fr(photo_name):
    # Библиотека
    import face_recognition
    import cv2

    image_processed = face_recognition.load_image_file(photo_name)
    face_location = face_recognition.face_locations(image_processed)
    img = cv2.imread(photo_name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    for(top, right, bottom, left) in (face_location):
        cv2.rectangle(img, (left, top), (right, bottom), (120,0,120), 2)
    plt.figure(figsize=(8,8), dpi=90)
    plt.imshow(img)
    plt.show()
    cv2.waitKey(0)
    
if __name__ == "__main__":
    main()