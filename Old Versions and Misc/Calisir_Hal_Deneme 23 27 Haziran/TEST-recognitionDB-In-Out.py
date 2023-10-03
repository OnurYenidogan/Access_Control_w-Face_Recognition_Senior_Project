import cv2
import os
import math
import sys
import face_recognition
import numpy as np
from some_functions import DBconn
from tkinter import Tk, Label, Button, TclError
from PIL import Image, ImageTk, ImageDraw, ImageFont
from datetime import datetime
from pathlib import Path

global Kamera_Tipi
Kamera_Tipi = 't'
global camera_id
camera_id = 2


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
    current_frame = None
    modified_frame = None  # This frame will include modifications

    def get_known_faces_from_db(self):
        known_face_ids = []
        known_face_encodings = []
        known_face_names = []

        with conn.cursor() as cur:
            cur.execute('SELECT id, name, encoding FROM faces')
            rows = cur.fetchall()

            for row in rows:
                face_id = row[0]
                name = row[1]
                encoding_bytes = row[2]
                encoding = np.frombuffer(encoding_bytes, dtype=np.float64)

                known_face_ids.append(face_id)
                known_face_encodings.append(encoding)
                known_face_names.append(name)
        return known_face_ids, known_face_encodings, known_face_names

    def screenshot(self):
        print("Screenshot button pressed!")  # Log that the button was pressed

        # Define the directory
        dir_path = Path(r"D:/KBÜ Computer Engineering/CE 2022-2023 Bahar/Bitirme Projesi II/test ss")

        # Check if the directory exists and is writable
        if not dir_path.exists():
            print(f"The directory {dir_path} does not exist. Trying to create it.")
            dir_path.mkdir(parents=True, exist_ok=True)
        if not os.access(dir_path, os.W_OK):
            print(f"The directory {dir_path} is not writable.")
            return

        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")

        # Create the file path
        file_path = dir_path / f"screenshot_{timestamp}.jpg"

        # Check the modified frame data
        if self.modified_frame is None:
            print("modified_frame is None. Can't save screenshot.")
            return
        print(f"modified_frame shape: {self.modified_frame.shape}, dtype: {self.modified_frame.dtype}")

        # Convert the frame back to BGR format for saving with PIL
        bgr_frame = cv2.cvtColor(self.modified_frame, cv2.COLOR_RGB2BGR)  # Added this line

        # Create a PIL Image object
        img = Image.fromarray(bgr_frame)

        # Try to save the image
        try:
            img.save(str(file_path))
            print(f"Screenshot saved successfully to {file_path}")
        except Exception as e:
            print(f"Failed to save screenshot: {e}")


    def run_recognition(self):
        self.known_face_ids, self.known_face_encodings, self.known_face_names = self.get_known_faces_from_db()
        video_capture = cv2.VideoCapture(camera_id)

        if not video_capture.isOpened():
            sys.exit('Video source not found...')

        root = Tk()
        label = Label(root)
        label.pack()

        # Screenshot button
        screenshot_button = Button(root, text="Screenshot", command=self.screenshot, width=200, height=200)
        screenshot_button.pack()

        text_height = 0
        text_width = 0

        while True:
            try:
                if not root.winfo_exists():
                    break
            except TclError:
                break
            ret, frame = video_capture.read()
            self.current_frame = frame
            self.modified_frame = frame.copy()  # Make a copy of the frame for modifications
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

                pil_image = Image.fromarray(rgb_frame)  # BGR to RGB conversion

                draw = ImageDraw.Draw(pil_image)

                font = ImageFont.truetype("arial.ttf", 20)  # Change font to arial and its size to 20

                padding = 10  # Increase or decrease for more or less padding
                text_width, text_height = draw.textbbox((0, 0), name, font=font)[2:4]

                # Draw a box around the face
                draw.rectangle(((left, top), (right, bottom)), outline=(0, 255, 0), width=2)

                # Draw a label with a name below the face
                draw.rectangle(((left - padding, bottom + padding),
                                (left + text_width + padding, bottom + text_height + 2 * padding)), fill=(255, 0, 0))
                draw.text((left, bottom + padding), name, font=font, fill=(255, 255, 255, 255))

                # Convert the image back to BGR for displaying with opencv
                rgb_frame = np.array(pil_image)
                self.modified_frame = np.array(pil_image)  # Save the modifications
                self.modified_frame = cv2.cvtColor(self.modified_frame, cv2.COLOR_BGR2RGB)

                raw_name = name.split(" (")[0]
                if 'Unknown' not in raw_name:
                    face_id = self.known_face_ids[self.known_face_names.index(raw_name)]

            rgb_frame = cv2.cvtColor(self.modified_frame, cv2.COLOR_BGR2RGB)

            image = Image.fromarray(rgb_frame)
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
