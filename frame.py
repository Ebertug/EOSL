import cv2
import os

video_path = 'video.mp4'
output_folder = 'frames'
os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)

frame_count = 0

saved_frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if frame_count % 5 == 0:
        frame_filename = os.path.join(output_folder, f'frame_{saved_frame_count:04d}.png')

        cv2.imwrite(frame_filename, frame)

        saved_frame_count += 1

    frame_count += 1

cap.release()

print(f'Toplam {saved_frame_count} frame kaydedildi.')
