import cv2
import psycopg2
import numpy as np

def get_camera_list():
    camera_list = []
    index = 0
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cap.read()[0]:
            break
        else:
            camera_name = index
            camera_list.append(camera_name)
        cap.release()
        index += 1
    return camera_list

def DBconn(hostname, database, username, pwd, port_id):
    conn = psycopg2.connect(
        host=hostname,
        database=database,
        user=username,
        password=pwd,
        port=port_id
    )
    return conn


def get_known_faces_from_db(conn):
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
    return  known_face_names, known_face_encodings