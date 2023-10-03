import cv2

# OpenCV yüz tespitçisi (face detector) yükleniyor
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Kamera bağlantısı başlatılıyor
video_capture = cv2.VideoCapture(1)

kucultmeOrani = 2  # İstediğiniz küçültme oranını buraya girin

while True:
    # Kameradan bir kare alınıyor
    ret, frame = video_capture.read()

    # Kareyi küçültme
    frame = cv2.resize(frame, (0, 0), fx=1/kucultmeOrani, fy=1/kucultmeOrani)

    # Kareyi gri tonlamaya dönüştürme
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Yüz tespiti yapma
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Tespit edilen yüzleri dikdörtgenle çevreleme
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Sonuçları gösterme
    cv2.imshow('Face Detection', frame)

    # 'q' tuşuna basıldığında döngüden çıkma
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırakma
video_capture.release()
cv2.destroyAllWindows()
