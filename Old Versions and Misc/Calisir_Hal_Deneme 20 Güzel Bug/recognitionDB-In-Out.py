import cv2
import math
import sys
import face_recognition
import numpy as np
from datetime import datetime
from some_functions import DBconn
from tkinter import Tk, Label, TclError
from PIL import Image, ImageTk, ImageDraw, ImageFont

global Kamera_Tipi
if sys.argv[2] == "TypeA":
    Kamera_Tipi = 'i'
else:
    Kamera_Tipi = 'o'


def add_to_database(face_id):
    cur = conn.cursor()

    # Get current datetime
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # Insert into log table
    cur.execute("INSERT INTO log (face_id, datetime, action) VALUES (%s, %s, %s)", (face_id, current_time, Kamera_Tipi))

    # Update faces table
    cur.execute("UPDATE faces SET status = %s, last_reco = %s WHERE id = %s", (Kamera_Tipi, current_time, face_id))

    # Commit changes
    conn.commit()
    print(face_id)

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

        known_face_ids = []
        known_face_encodings = []
        known_face_names = []

        with conn.cursor() as cur:
            # SELECT sorgusu ile 'faces' tablosundaki tüm satırları al
            cur.execute('SELECT id, name, encoding FROM faces')

            # Tüm satırları al
            rows = cur.fetchall()

            # Her satırı döngüde işle
            for row in rows:
                face_id = row[0]
                name = row[1]
                encoding_bytes = row[2]
                encoding = np.frombuffer(encoding_bytes, dtype=np.float64)

                known_face_ids.append(face_id)
                known_face_encodings.append(encoding)
                known_face_names.append(name)
        return known_face_ids, known_face_encodings, known_face_names

    # Veritabanından yüz verilerini çek
    #known_face_encodings, known_face_names = get_known_faces_from_db()

    # İşlem bittiğinde veritabanı bağlantısını kapattık
    def run_recognition(self):

        self.known_face_ids, self.known_face_encodings, self.known_face_names = self.get_known_faces_from_db()
        video_capture = cv2.VideoCapture(int(sys.argv[1]))

        if not video_capture.isOpened():
            sys.exit('Video source not found...')

        root = Tk()
        label = Label(root)
        label.pack()

        text_height = 0
        text_width = 0

        while True:
            try:
                if not root.winfo_exists():
                    break
            except TclError:
                break
            ret, frame = video_capture.read()
            kucultmeOranı = 1  # detection daha küçük ölçekte yapılır

            small_frame = frame
            small_frame = cv2.resize(frame, (0, 0), fx=1 / kucultmeOranı, fy=1 / kucultmeOranı)

            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.face_locations = face_recognition.face_locations(rgb_small_frame)

            self.face_encodings = face_recognition.face_encodings(rgb_frame, [
                (top * kucultmeOranı, right * kucultmeOranı, bottom * kucultmeOranı, left * kucultmeOranı) for
                top, right, bottom, left in self.face_locations])

            self.face_names = []
            for face_encoding in self.face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                confidence = '???'
                yazdirmalikName = "Unknown"

                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    yazdirmalikName = name
                    confidence = face_confidence(face_distances[best_match_index])

                self.face_names.append(f'{name} ({confidence})')

            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= kucultmeOranı
                right *= kucultmeOranı
                bottom *= kucultmeOranı
                left *= kucultmeOranı

                pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                draw = ImageDraw.Draw(pil_image)

                font = ImageFont.load_default()

                text_bbox = draw.textbbox((left + 6, bottom - text_height - 5), name, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255))
                draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

                frame = np.array(pil_image)

                raw_name = name.split(" (")[0]
                if 'Unknown' not in raw_name:
                    face_id = self.known_face_ids[self.known_face_names.index(raw_name)]
                    add_to_database(face_id)

            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image)

            label.config(image=photo)
            label.image = photo

            root.update()

            if cv2.waitKey(1) == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()



if __name__ == '__main__':
    global conn
    conn = DBconn()

    fr = FaceRecognition()
    fr.run_recognition()