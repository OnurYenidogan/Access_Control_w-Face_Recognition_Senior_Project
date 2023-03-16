import psycopg2
import psycopg2.extras
import face_recognition
import os, sys
import cv2
import numpy as np
import math



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

                    cur.execute(insert_script, (image, face_encoding_bytes))

        except Exception as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        known_face_encodings.append(face_encoding)
        known_face_names.append(image)
    print(known_face_names)