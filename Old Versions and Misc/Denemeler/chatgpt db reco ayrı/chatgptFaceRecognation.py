import face_recognition
import cv2

import dlib


import psycopg2
import numpy as np

def get_known_faces_from_db():
    # Veritabanına bağlanma bilgilerini buraya girin
    hostname = 'localhost'
    database = 'SeniorProject'
    username = 'postgres'
    pwd = '1234'
    port_id = 5432

    known_face_encodings = []
    known_face_names = []

    # Veritabanına bağlan
    with psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id) as conn:
        # Veritabanı işlemleri için cursor oluştur
        with conn.cursor() as cur:
            # SELECT sorgusu ile 'faces' tablosundaki tüm satırları al
            cur.execute('SELECT name, encoding FROM faces')

            # Tüm satırları al
            rows = cur.fetchall()
            print(rows)
            # Her satırı döngüde işle
            for row in rows:
                name = row[0]
                encoding_bytes = row[1]
                encoding = np.frombuffer(encoding_bytes, dtype=np.float64)
                known_face_encodings.append(encoding)
                known_face_names.append(name)
    print(known_face_encodings)
    return known_face_encodings, known_face_names

# Veritabanından yüz verilerini çek
known_face_encodings, known_face_names = get_known_faces_from_db()

# İşlem bittiğinde veritabanı bağlantısını kapattık

def live_face_recognition(face_encodings, face_names):
    """
    Verilen yüz kodları ve isimler kullanılarak canlı kamera akışında yüz tanıma yapar.
    """
    # Dlib yüz tanıma sınıflandırıcısını yükle
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # Kamera bağlantısını başlat
    cap = cv2.VideoCapture(0)

    while True:
        # Kameradan bir kare yakala
        ret, frame = cap.read()

        # Kareyi griye dönüştür
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Yüzleri tespit et
        faces = detector(gray, 0)

        # Her tespit edilen yüz için
        for face in faces:
            # Yüzü çerçeve içine al
            (x, y, w, h) = (face.left(), face.top(), face.right() - face.left(), face.bottom() - face.top())

            # Yüzün özniteliklerini hesapla
            face_descriptor = face_recognition.face_encodings(frame, [face])[0]

            # Yüzü tanı
            matches = face_recognition.compare_faces(face_encodings, face_descriptor)
            name = "Unknown"

            # En yakın eşleşen yüzü bul
            face_distances = face_recognition.face_distance(face_encodings, face_descriptor)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = face_names[best_match_index]

            # Yüzün çevresine kutu çiz ve ismini yaz
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        # Ekranı göster
        cv2.imshow('Live Face Recognition', frame)

        # "q" tuşuna basılana kadar devam et
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Belleği serbest bırak ve kamerayı kapat
    cap.release()
    cv2.destroyAllWindows()

live_face_recognition(get_known_faces_from_db())