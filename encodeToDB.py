import psycopg2
import psycopg2.extras
import face_recognition
import os, sys
import cv2
import numpy as np
import math



hostname = 'localhost'
database = 'SeniorProject'
username = 'postgres'
pwd = '1234'
port_id = 5432
conn = None

try:
    with psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            """cur.execute('DROP TABLE IF EXISTS faces')"""

            create_script = ''' CREATE TABLE IF NOT EXISTS faces (
                                    id      int PRIMARY KEY,
                                    name    varchar(100) NOT NULL,
                                    encoding BYTEA '''
            cur.execute(create_script)

            insert_script  = 'INSERT INTO faces (id, name, encoding) VALUES (%s, %s, %s, %s)'
            insert_values = [(1, 'James', 12000, 'D1'), (2, 'Robin', 15000, 'D1'), (3, 'Xavier', 20000, 'D2')]
            for record in insert_values:
                cur.execute(insert_script, record)

except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()


def encode_faces(path):
    known_face_encodings = []
    known_face_names = []
    for image in os.listdir(path):
        face_image = face_recognition.load_image_file(f"../Faces/{image}")
        face_encodings = face_recognition.face_encodings(face_image)

        # Skip image if no faces are detected
        if len(face_encodings) == 0:
            print(f"No faces detected in image {image}. Skipping.")
            continue
        face_encoding = face_encodings[0]

        known_face_encodings.append(face_encoding)
        known_face_names.append(image)
    print(known_face_names)