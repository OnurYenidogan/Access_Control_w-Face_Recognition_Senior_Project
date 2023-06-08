import psycopg2
import psycopg2.extras
import face_recognition
import os
import numpy as np
from tkinter import filedialog, messagebox


def encode_faces():
    folder_path = filedialog.askdirectory()

    if not folder_path:
        # Kullanıcı bir dizin seçmediği için fonksiyonu sonlandırın
        return

    known_face_encodings = []
    known_face_names = []
    for image in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image)  # construct full image path
        face_image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(face_image)

        # Skip image if no faces are detected
        if len(face_encodings) == 0:
            print(f"No faces detected in image {image}. Skipping.")
            continue

        face_encoding = face_encodings[0]
        if len(face_encodings) == 0:
            print("No faces found in the image")
            return

        # Convert the encoding to a binary representation
        face_encoding_bytes = np.array(face_encodings[0]).tobytes()

        hostname = 'localhost'
        database = 'SeniorProject'
        username = 'postgres'
        pwd = '1234'
        port_id = 5432
        conn = None

        try:
            with psycopg2.connect(
                    host=hostname,
                    dbname=database,
                    user=username,
                    password=pwd,
                    port=port_id) as conn:

                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    """cur.execute('DROP TABLE IF EXISTS faces')"""

                    create_script = ''' CREATE TABLE IF NOT EXISTS faces (
                                                    id SERIAL PRIMARY KEY,
                                                    name    varchar(100) NOT NULL,
                                                    encoding BYTEA )'''
                    cur.execute(create_script)
                    insert_script = 'INSERT INTO faces (name, encoding) VALUES (%s, %s)'
                    # Get the file name without the extension
                    name = os.path.splitext(image)[0]
                    cur.execute(insert_script, (name, face_encoding_bytes))
        except Exception as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        known_face_encodings.append(face_encoding)
        known_face_names.append(name)

        # Her bir yüzün veritabanına eklenmesi durumunda bir mesaj gösteren bir iletişim kutusu açın
        # msg = f"{name} added to the database."
        # messagebox.showinfo(title="Face encoded", message=msg)

    # Yüzlerin sayısını gösteren bir iletişim kutusu açın
    msg = f"{len(known_face_names)} kişi veritabanına kaydedildi."
    messagebox.showinfo(title="Process completed", message=msg)


def stop_program():
    exit()


if __name__ == '__main__':
    encode_faces()
