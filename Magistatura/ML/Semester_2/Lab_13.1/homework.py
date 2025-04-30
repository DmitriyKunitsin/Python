# Сегментация - разделение изоражения на области, которые относятся к каждому объекту
from ultralytics import YOLO 
import cv2

def main():
    # Модель для сегментации
    model = YOLO("yolov8x-seg.pt")
    # Предсказание
    results = model.predict(source="..\img_and_video\one.jpg", save=True, save_crop=True, project="runs/detect", name="inference", exist_ok=True)

    # Сегментация видео    
    segmentation_video("..\img_and_video\input_video.mp4")
    # Конверт видео
    convert_avi_to_mp4(r"./result_video.avi")
                       
def segmentation_video(path_video):
    from ultralytics import solutions
    cap = cv2.VideoCapture(path_video)
    assert cap.isOpened() , "Ошибка чтения видео"
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    video_writer = cv2.VideoWriter("result_video.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w,h))

    isegment = solutions.InstanceSegmentation(
        show=True,
        model="yolo11n-seg.pt",
        conf=0.6,
        verbose=False
    )

    while cap.isOpened():
        success, im0 = cap.read()
        if not success:
            print("Видео кончилось")
            break
        results = isegment(im0)
        video_writer.write(results.plot_im)
    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()

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

if __name__ == '__main__':
    main()