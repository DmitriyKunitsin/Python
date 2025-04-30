# Сегментация - разделение изоражения на области, которые относятся к каждому объекту
from ultralytics import YOLO 

def main():
    model = YOLO("yolov8n.pt")

if __name__ == '__main__':
    main()