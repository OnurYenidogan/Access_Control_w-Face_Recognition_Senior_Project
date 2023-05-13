import math
import sys
import cv2
import face_recognition
import numpy as np
import psycopg2.extras
import psycopg2
from datetime import datetime
from some_functions import DBconn

global Kamera_Tipi
if sys.argv[2] == "TypeA":
    Kamera_Tipi = 'i'
else:
    Kamera_Tipi = 'o'


def add_to_database(name):
    #conn = psycopg2.connect(database="your_database_name", user="your_username", password="your_password", host="your_host", port="your_port")
    cur = conn.cursor()

    # Şimdiki datetime bilgisini al
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # Veritabanına ekleme işlemi
    cur.execute("INSERT INTO log (name, datetime, action) VALUES (%s, %s, %s)", (name, current_time, Kamera_Tipi))
    cur.execute("UPDATE faces SET Status = %s, last_reco = %s WHERE name = %s", (Kamera_Tipi, current_time,name))

    # Değişiklikleri kaydetme
    conn.commit()
    print(name)
    # Bağlantıyı kapat



# Fonksiyonu kullanarak veritabanına kayıt ekleme


# Helper
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []


    def get_known_faces_from_db(self):

        known_face_encodings = []
        known_face_names = []

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
        return known_face_encodings, known_face_names

    # Veritabanından yüz verilerini çek
    #known_face_encodings, known_face_names = get_known_faces_from_db()

    # İşlem bittiğinde veritabanı bağlantısını kapattık
    def run_recognition(self):

        self.known_face_encodings, self.known_face_names = self.get_known_faces_from_db()
        video_capture = cv2.VideoCapture(int(sys.argv[1]))

        if not video_capture.isOpened():
            sys.exit('Video source not found...')

        # OpenCV yüz tespitçisi (face detector) yükleniyor
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        while True:
            ret, frame = video_capture.read()
            kucultmeOranı = 1
            small_frame = frame
            small_frame = cv2.resize(frame, (0, 0), fx=1 / kucultmeOranı, fy=1 / kucultmeOranı)

            gray_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

            # Yüz tespiti yapma
            self.face_locations = face_cascade.detectMultiScale(gray_small_frame, scaleFactor=1.1, minNeighbors=5,
                                                                minSize=(30, 30))

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            rgb_frame = frame[:, :, ::-1]

            # Correct this line
            self.face_encodings = face_recognition.face_encodings(
                rgb_frame,
                [(y * kucultmeOranı, (x + w) * kucultmeOranı, (y + h) * kucultmeOranı, x * kucultmeOranı) for
                 (x, y, w, h) in self.face_locations]
            )

            self.face_names = []
            for face_encoding in self.face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                confidence = '???'
                yazdirmalikName = "Unknown"  # Initialize it here

                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    yazdirmalikName = name
                    confidence = face_confidence(face_distances[best_match_index])

                self.face_names.append(f'{name} ({confidence})')

            # Display the results
            for (x, y, w, h), name in zip(self.face_locations, self.face_names):
                top, right, bottom, left = y, x + w, y + h, x
                top *= kucultmeOranı
                right *= kucultmeOranı
                bottom *= kucultmeOranı
                left *= kucultmeOranı

                # Create the frame with the name
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

                if yazdirmalikName != 'Unknown':
                    add_to_database(yazdirmalikName)

                # Display the resulting image
            if Kamera_Tipi == 'i':
                Baslik = "Cam " + sys.argv[1] + " Entry"
            else:
                Baslik = "Cam " + sys.argv[1] + " Exit"
            cv2.imshow(Baslik + ' Face Reco', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    global conn
    conn = DBconn()

    fr = FaceRecognition()
    fr.run_recognition()
