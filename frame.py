import cv2
import os

# Videoların bulunduğu klasör
videos_folder = 'videos'

# Tüm video dosyalarını listele
video_files = [f for f in os.listdir(videos_folder) if f.endswith('.mp4')]

# Her bir video dosyası için işlemleri sırayla yap
for video_file in video_files:
    # Video dosyasının tam yolu
    video_path = os.path.join(videos_folder, video_file)

    # Video adını dosya uzantısı olmadan al
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Videonun adıyla bir klasör oluştur
    output_folder = video_name
    os.makedirs(output_folder, exist_ok=True)

    # Videoyu yükle
    cap = cv2.VideoCapture(video_path)

    # Frame numarasını takip etmek için sayaç
    frame_count = 0

    # Kaydedilen frameleri takip etmek için sayaç
    saved_frame_count = 0

    # Videodaki tüm frameleri oku ve kaydet
    while True:
        ret, frame = cap.read()

        # Eğer video bitti ise, döngüyü sonlandır
        if not ret:
            break

        # Her 5 framede bir kaydet
        if frame_count % 4 == 0:
            # Frame dosya adı
            frame_filename = os.path.join(output_folder, f'{video_name}_{saved_frame_count:04d}.png')

            # Frame'i kaydet
            cv2.imwrite(frame_filename, frame)

            # Kaydedilen frame sayısını arttır
            saved_frame_count += 1

        # Frame numarasını arttır
        frame_count += 1

    # Video kaynağını serbest bırak
    cap.release()

    print(f"Toplam {saved_frame_count} frame '{output_folder}' klasörüne kaydedildi.")
