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

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
def get_search_classes(dict, need_classes):

    valid_classes = {}
    for val in need_classes:
        key = get_key(dict, val)
        if  key is not None:
            valid_classes[key] = dict[key]
    return list(valid_classes.keys())

def detect_photo(path, need_classes = []):
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    from ultralytics import YOLO
    import os

    model = YOLO("yolov8x.pt")
    need_classes = [val for key , val in  model.names.items()] if not need_classes else need_classes  
    detected_classes = get_search_classes(model.names, need_classes)
    photos = list(filter(lambda x : '.png' in x, os.listdir(path)))
    for photo in photos:
        photo = os.path.join(path, photo)
        resluts = model.predict(source=photo, classes=detected_classes)
        result = resluts[0]

        image = cv2.imread(photo)

        for box in result.boxes:
            class_id = result.names[box.cls[0].item()]
            cords = box.xyxy[0].tolist()
            cords = [round(x) for x in cords] 
            conf = round(box.conf[0].item(), 2)

            cv2.rectangle(image, (cords[0], cords[1]), (cords[2], cords[3]), (0,255,0), 2)

            label = f"{class_id} {conf}"
            cv2.putText(image, label, (cords[0], cords[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (40, 38, 200), 2)
        
        plt.figure(figsize=(8,8), dpi=90)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.show()
        cv2.waitKey(0)
    

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
    """
        https://docs.ultralytics.com/ru/modes/train/#train-settings
        Дока по трейну
        ТАм все доступные аргументы с описанием    
    """
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
    """
        https://docs.ultralytics.com/ru/modes/predict/#inference-arguments
        Дока по предикту
        ТАм все доступные аргументы с описанием    
    """
    predict = model.predict(
    source="face_predict_video.mp4", 
    imgsz=(1280, 1080),                                                 
    hide_labels=False,                                           
    save=True,                                                  
    name="results",                                                 
    conf=0.25,       
    max_det=3,
    verbose=True                                            
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
import time
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"  

path_date = ''
def main():
    # Ищу мишек на фотке без ограничей в классах поиска
    # print(f'{GREEN}Начало работы программы{RESET}')
    # strat_time = time.time()
    # detect_photo(r'bear_dog_photo')
    # end_time = time.time()
    # print(f'{GREEN}Время выполнения детекции фото {RED}{end_time-strat_time}{GREEN} секунд{RESET}')
    
    # Ищу 2 определенных класса
    # strat_time = time.time()
    # detect_classes = {'bear', 'cat'}
    # detect_photo(r'animals', detect_classes)
    # end_time = time.time()
    # print(f'{GREEN}Время выполнения детекции фото 2 классов  {RED}{end_time-strat_time}{GREEN} секунд{RESET}')

    # Генерирую данные для обучения модели
    # strat_time = time.time()
    # dataset_generation()
    # end_time = time.time()
    # print(f'{GREEN}Время выполнения генерации данных для обучения {RED}{end_time-strat_time}{GREEN} секунд{RESET}')

    # Обучаю модель на видео
    # strat_time = time.time()
    # train_model()
    # end_time = time.time()
    # print(f'{GREEN}Время выполнения обучения модели {RED}{end_time-strat_time}{GREEN} секунд{RESET}')

    # Предсказываю и указываю где лица
    # strat_time = time.time()
    # predict_model()
    # end_time = time.time()
    # print(f'{GREEN}Время выполнения предсказания {RED}{end_time-strat_time}{GREEN} секунд{RESET}')

    # Конвертирую форматы видео
    # strat_time = time.time()
    # convert_avi_to_mp4(r"runs\detect\results2\face_predict_video.avi")
    # end_time = time.time()
    # print(f'{GREEN}Время выполнения конвертация формата {RED}{end_time-strat_time}{GREEN} секунд{RESET}')

if __name__ == "__main__":
    main()



