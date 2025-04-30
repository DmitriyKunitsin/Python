# Отслеживание траекторий
from ultralytics import YOLO
import cv2
from collections import defaultdict
import numpy as np


def main():
    # check_traectory(r"..\img_and_video\cork.mp4", r"./result_video.avi")

    convert_avi_to_mp4(r"./result_video.avi")

def check_traectory(path_video, output_path):
    model = YOLO("yolo11n.pt")

    cap = cv2.VideoCapture(path_video)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    lenght = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    number_frame = 0
    track_history = defaultdict(lambda : [])

    while cap.isOpened():
        success, frame = cap.read()
        number_frame += 1

        if success:
            result = model.track(frame, persist=True, show=False, conf=0.5, verbose=False)[0]

            if result.boxes and result.boxes.id is not None:

                boxes = result.boxes.xywh.cpu()
                track_ids = result.boxes.id.int().cpu().tolist()

                frame = result.plot()

                for box, track_id in zip(boxes, track_ids):
                    x,y,w,h = box
                    track = track_history[track_id]
                    track.append((float(x), float(y)))
                    if len(track) > 45:
                        track.pop(0)
                    
                    points = np.hstack(track).astype(np.int32).reshape((-1,1,2))
                    cv2.polylines(frame, [points], isClosed=False, color=(230,230,230), thickness=10)
                out.write(frame)
                print(f'Кадр {number_frame}/{lenght} успешно записан')
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f'Результирующее видео сохранено по пути : {output_path}')

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

if __name__ == "__main__":
    main()