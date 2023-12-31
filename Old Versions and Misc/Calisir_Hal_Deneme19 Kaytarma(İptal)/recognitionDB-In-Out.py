import math
import sys
import cv2
import face_recognition
import numpy as np
from datetime import datetime
from some_functions import DBconn

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

        while True:
            ret, frame = video_capture.read()
            kucultmeOranı=1#detection daha küçük ölçekte yapılır
            # Only process every other frame of video to save time
            #if self.process_current_frame:
            small_frame = frame
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=1/kucultmeOranı, fy=1/kucultmeOranı)


            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            rgb_frame = frame[:, :, ::-1]
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)

            self.face_encodings = face_recognition.face_encodings(rgb_frame, [(top*kucultmeOranı, right*kucultmeOranı, bottom*kucultmeOranı, left*kucultmeOranı) for top, right, bottom, left in self.face_locations])

            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                confidence = '???'
                yazdirmalikName = "Unknown"  # Initialize it here

                # Calculate the shortest distance to face
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    face_id = self.known_face_ids[best_match_index]  # This is where we get the correct face_id
                    name = self.known_face_names[best_match_index]
                    yazdirmalikName = name
                    confidence = face_confidence(face_distances[best_match_index])

                self.face_names.append(f'{name} ({confidence})')

            #self.process_current_frame = not self.process_current_frame

            # Display the results
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= kucultmeOranı
                right *= kucultmeOranı
                bottom *= kucultmeOranı
                left *= kucultmeOranı

                # Frame thickness
                frame_thickness = 2

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0),
                              frame_thickness)  # Change the color to red

                # Calculate text width & height to draw the transparent boxes
                font = cv2.FONT_HERSHEY_DUPLEX
                font_scale = 0.68
                font_thickness = 1
                text_size = cv2.getTextSize(name, font, font_scale, font_thickness)[0]

                # Scale factors for width and height
                scale_factor = 1.2  # Adjust this value to your preference

                # Draw a filled box around the name
                padding = int(scale_factor * 5)  # Adjust this value to your preference
                text_offset_x = left
                text_offset_y = bottom + frame_thickness + int(
                    text_size[1] * scale_factor) + padding  # Adjust for frame thickness
                box_coords = ((text_offset_x - padding, text_offset_y + padding),
                              (text_offset_x + text_size[0] + padding,
                               text_offset_y - int(text_size[1] * scale_factor) - padding))
                cv2.rectangle(frame, box_coords[0], box_coords[1], (0, 0, 255), cv2.FILLED)  # Change the color to green

                # Draw the text
                cv2.putText(frame, name, (text_offset_x, text_offset_y - padding), font, font_scale, (255, 255, 255),
                            font_thickness)

                if yazdirmalikName != 'Unknown':
                    add_to_database(face_id)

            # Display the resulting image
            if Kamera_Tipi == 'i' :
                Baslik = "Cam "+sys.argv[1]+" Entry"
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
