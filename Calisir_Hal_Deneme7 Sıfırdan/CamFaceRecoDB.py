import math
import face_recognition
import sys
import cv2
import numpy as np
from datetime import datetime

def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

def camReco(person_list, cam_No,conn):
    known_face_names, known_face_encodings = person_list
    video_capture = cv2.VideoCapture(cam_No)

    if not video_capture.isOpened():
        sys.exit('Video source not found...')

    while True:
        ret, frame = video_capture.read()

        # Only process every other frame of video to save time
        # if self.process_current_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        small_frame = frame

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            confidence = '???'

            # Calculate the shortest distance to face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                yazdirmalikName = name
                confidence = face_confidence(face_distances[best_match_index])

            face_names.append(f'{name} ({confidence})')

        # self.process_current_frame = not self.process_current_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            """top *= 4
            right *= 4
            bottom *= 4
            left *= 4"""

            # Create the frame with the name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            if yazdirmalikName != 'Unknown':
                # conn = psycopg2.connect(database="your_database_name", user="your_username", password="your_password", host="your_host", port="your_port")
                cur = conn.cursor()
                Kamera_Tipi = 'i'
                # Şimdiki datetime bilgisini al
                now = datetime.now()
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")

                # Veritabanına ekleme işlemi
                cur.execute("INSERT INTO log (name, datetime, action) VALUES (%s, %s, %s)",
                            (yazdirmalikName, current_time, Kamera_Tipi))
                cur.execute("UPDATE faces SET Status = 'i', last_reco = %s WHERE name = %s", (current_time, yazdirmalikName))

                # Değişiklikleri kaydetme
                conn.commit()

        # Display the resulting image

        cv2.imshow('Face Recognition' + str(cam_No), frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()