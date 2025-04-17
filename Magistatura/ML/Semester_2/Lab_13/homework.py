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
    Виды размеров : Nano (*n.pt), Small (*s.pt), Medium (*m.pt), Large (*l.pt), Huge (*x.pt)
        Чем больше модель, тем лучше качество предсканаия можно добится, но тем медленей будет работать
"""
def dataset_generation():
    import os 
    import numpy as np
    os.getcwd()

    folder_train_img = 'datasets/train/images'
    folder_train_lab = 'datasets/train/labels'
    folder_val_img = 'datasets/val/images'
    folder_val_lab = 'datasets/val/labels'

    if  os.path.exists('datasets'):
        import shutil
        shutil.rmtree('datasets')
        shutil.rmtree('runs')

    os.mkdir('runs')
    os.makedirs(folder_train_img, exist_ok=True)
    os.makedirs(folder_train_lab, exist_ok=True)
    os.makedirs(folder_val_img, exist_ok=True)
    os.makedirs(folder_val_lab, exist_ok=True)


    import face_recognition
    import cv2

    input_movie = cv2.VideoCapture('faces_train_video.mp4')
    frame_number = 0

    lenght = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

    while True:

        ret, frame = input_movie.read()

        frame_number += 1
        if not ret:
            print(f'На кадре {frame_number} все кончилось')
            break
        rgb_small_frame = np.ascontiguousarray(frame[:, :, ::-1])

        face_locations= face_recognition.face_locations(rgb_small_frame)

        print(f'Лиц найденo {len(face_locations)} в кадре {frame_number}')
        folder_write = (folder_train_img, folder_train_lab) if frame_number % 2 == 0 else (folder_val_img, folder_val_lab)
        image_folder, label_folder = folder_write

        if(len(face_locations) > 0):
            cv2.imwrite(os.path.join(image_folder,f"image_{frame_number}.png"),img=frame)
            with open(os.path.join(label_folder,f"image_{frame_number}.txt"), "w") as newfile:
                for (top, right, bottom, left) in (face_locations):  
                    center_x = (left + right) / 2 / frame.shape[1]
                    center_y = (top + bottom) / 2 / frame.shape[0]
                    width = (right - left) / frame.shape[1]
                    height = (bottom - top) / frame.shape[0]   
                    newfile.writelines(f"0 {center_x} {center_y} {width} {height}\n")
                
        print(f"Кадр {frame_number} / {lenght} обработан")

    with open(f"runs/face.yaml", "w") as finalfile:
        finalfile.writelines(f"train: {folder_train_img}\n")
        finalfile.writelines(f"val: {folder_val_img}\n")
        finalfile.writelines("\n")
        finalfile.writelines("# Classes \n")
        finalfile.writelines(f"nc: {1}\n")
        finalfile.writelines(f"names: ['faces']\n")
    print('Конец')

def train_model():

    model = YOLO("yolov8n.pt")
    
    results = model.train(
        data='./runs/face.yaml',
        imgsz=1280,
        epochs=5,
        batch=6,
        device='cpu',
        name='YOLOv8n'
    )

def predict_model():

    model = YOLO("runs/detect/YOLOv8n9/weights/best.pt")

    predict = model.predict(
    source="face_predict_video.mp4", 
    show=True,                                                  
    imgsz=1280,                                                 
    hide_labels=True,                                           
    save=True,                                                  
    name="results",                                                 
    conf=0.1,                                                   
    )

def convert_avi_to_mp4(avi_file_path):
    import os
    from time import time
    import moviepy as moviepy
    
    if not os.path.exists(avi_file_path):
        raise FileNotFoundError(avi_file_path)
    t0 = time()
    clip = moviepy.VideoFileClip(avi_file_path)
    path, file_name = os.path.split(avi_file_path)
    output_name = os.path.join(path, os.path.splitext(file_name)[0] + '.mp4')
    clip.write_videofile(output_name)
    print('Finished conversion in %is' % (time() - t0))

from ultralytics import YOLO

path_date = ''
def main():
    # Генерирую данные для обучения модели
    dataset_generation()

    # Обучаю модель на видео
    train_model()

    # Предсказываю и указываю где лица
    predict_model()

    # Конвертирую форматы видеоC:\Users\d.kunicin\Python\Python\Magistatura\ML\Semester_2\Lab_13\runs\detect\results\face_predict_video.avi
    convert_avi_to_mp4(r"runs\detect\results\face_predict_video.avi")

if __name__ == "__main__":
    main()



