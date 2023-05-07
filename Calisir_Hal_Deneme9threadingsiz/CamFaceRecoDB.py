import math
import face_recognition
import sys
import cv2
import numpy as np
from datetime import datetime
class camReco:
    def __init__(self, person_list, cam_No, conn):
        self.person_list = person_list
        self.cam_No = cam_No
        self.conn = conn
        self.known_face_names, self.known_face_encodings = self.person_list
        self.video_capture = cv2.VideoCapture(self.cam_No)

        if not self.video_capture.isOpened():
            sys.exit('Video source not found...')

    def face_confidence(self, face_distance_threshold=0.6):
        """
        Function to calculate the confidence value for a face match
        """
        if face_distance_threshold > 0.6:
            return "Low"
        elif face_distance_threshold > 0.45:
            return "Medium"
        else:
            return "High"

    def run(self):
        while True:
            ret, frame = self.video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            yazdirmalikName = "Unknown"
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                confidence = '???'

                # Calculate the shortest distance to face
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    yazdirmalikName = name
                    confidence = self.face_confidence(face_distances[best_match_index])

                face_names.append(f'{name} ({confidence})')

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Create the frame with the name
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

                if yazdirmalikName != 'Unknown':
                    # conn = psycopg2.connect(database="your_database_name", user="your_username", password="your_password", host="your_host", port="your_port")
                    cur = self.conn.cursor()
                    Kamera_Tipi = 'i'
                    # Şimdiki datetime bilgisini al
                    now = datetime.now()
                    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

                    # Veritabanına ekleme işlemi
                    cur.execute("INSERT INTO log (name, datetime, action) VALUES (%s, %s, %s)",
                                (yazdirmalikName, current_time, Kamera_Tipi))
                    cur.execute("UPDATE faces SET Status = 'i', last_reco = %s WHERE name = %s",
                                (current_time, yazdirmalikName))

                    # Değişiklikleri kaydetme
                    self.conn.commit()

                # Display the resulting image

            cv2.imshow('Face Recognition' + str(self.cam_No), frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) == ord('q'):
                break

        # Release handle to the webcam
        self.video_capture.release()
        cv2.destroyAllWindows()
