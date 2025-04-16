'''
    YOLO: Использование предобученной нейронной сети для детекции объектов. 
        Изучите приложенные ссылки. 
        Выберите подходящую для выполнения работы модель YOLO. 
        Загрузите произвольные фотографии с изображением объектов из набора предобученной нейронной сети. 
        Выполните дектекцию объектов и сделайте выводы (сеть обучена на картинках размером 640х640, 
        как она работает с изображениями других разрешений?). 
        Попробуйте детектировать только 2-а типа объектов, а не все 80, на которые рассчитана YOLO. 
        Проделайте такую же работу с видео. 
        Следующая часть работы связана с тестированием используемой модели. 
        Скачайте размеченный датасет. 
        Получите оценки точности работы YOLO - дайте пояснения используемым метрикам. 
        Сравните по точности и по времени работы две модели - nano и small. 

        1. Документация по ultralytics YOLOv8 : https://docs.ultralytics.com/ru
        2. Конфигурационный файл по умолчанию : https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/default.yaml
        3. Набор размеченных данных : https://storage.googleapis.com/openimages/web/visualizer/index.html?type=segmentation&set=train&r=false&c=%2Fm%2F0663v
        4. Перечень предобученных моделей и классов объектов : https://www.freecodecamp.org/news/how-to-detect-objects-in-images-using-yolov8/
        5. Пример дектекции предобученной моделью и обучение для пользовательских объектов : https://uproger.com/obuchaem-s-yolov8-na-polzovatelskih-dannyh-yolov8-instrukcziya-po-rabote/
        6. Пример детекции дорожных знаков : https://habr.com/ru/articles/754206/
        7. Пример использования ClassifAI для разметки данных : https://skine.ru/articles/54127/
        8. Набор данных COCO - возможно понадобится для скачивания меток классов : https://cocodataset.org/#home
'''

"""
    *model = YOLO("yolov8n.pt")*

    При первом запуске кода, он загрузит файл yolov8n.pt
        с сервера Ultralytics  в текущую папку
    Существует три типа модели и 5 моделей разного размера для каждого типа
    Виды моделей : Классификация (yolov8n-cls.pt), Обнаружение  (yolov8n.pt), Сегментация (yolov8n-seg.pt)
    Виды размеров : Nano, Small, Medium, Large, Huge
        Чем больше модель, тем лучше качество предсканаия можно добится, но тем медленей будет работать
"""
"""
    import os 
import numpy as np
os.getcwd()


# if not os.path.exists('yaml'):
# os.mkdir('yaml')
os.makedirs('yaml/train/images', exist_ok=True)
os.makedirs('yaml/train/labels', exist_ok=True)
os.makedirs('yaml/val/images', exist_ok=True)
os.makedirs('yaml/val/labels', exist_ok=True)

import face_recognition
import cv2

input_movie = cv2.VideoCapture('/content/test_video.mp4')
frame_number = 0


while True:

  ret, frame = input_movie.read()

  frame_number += 1
  if not ret:
    print(f'На кадре {frame_number} все кончилось')
    break
  rgb_small_frame = np.ascontiguousarray(frame[:, :, ::-1])

  face_locations= face_recognition.face_locations(rgb_small_frame)

  print(f'Лиц найденo {len(face_locations)}')
  



"""
from ultralytics import YOLO

def main():
    d = 1

if __name__ == "__main__":
    main()