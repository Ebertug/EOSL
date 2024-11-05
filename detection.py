import cv2
from ultralytics import YOLO
import pygame
from gtts import gTTS
import os
import threading

def text_to_speech(text):
    audio_file = 'output.mp3'
    tts = gTTS(text=text, lang='en')
    tts.save(audio_file)
    
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass  

    pygame.mixer.music.unload()  
    os.remove(audio_file)  

def speak_in_thread(text):
    threading.Thread(target=text_to_speech, args=(text,)).start()

def main():
    model = YOLO('best.pt')
    class_names = model.names  
    output_file = 'recognized_classes.txt'
    
    recognized_classes = set()
    last_class_name = None  
    
    cap = cv2.VideoCapture(0)
    with open(output_file, "w") as f:
        pass
    while True:
        
        ret, frame = cap.read()
        if not ret:
            break
        
        results = model(frame)
        for result in results:
            boxes = result.boxes 
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = box.conf[0]  
                cls = int(box.cls[0])
                
                class_name = class_names[cls] if cls < len(class_names) else 'Unknown Word'

                if class_name != last_class_name:
                    recognized_classes.add(class_name)
                    last_class_name = class_name  
                    speak_in_thread(class_name)
                
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f'Class: {class_name}, Conf: {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow('YOLOv8 Object Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

    with open('recognized_classes.txt', 'w') as f:
        for class_name in recognized_classes:
            f.write(f"{class_name}\n")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
