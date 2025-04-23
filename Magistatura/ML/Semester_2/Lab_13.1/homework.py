# Сегментация - разделение изоражения на области, которые относятся к каждому объекту
from ultralytics import YOLO 

def main():
    # Модель для сегментации
    model = YOLO("yolov8x-seg.pt")
    # # Предсказание
    results = model.predict(source="..\img_and_video\one.jpg", save=True, save_crop=True, project="runs/detect", name="inference", exist_ok=True)
    # import os 
    # print(os.path.isfile(r"..\img_and_video\one.jpg"))
    

if __name__ == '__main__':
    main()