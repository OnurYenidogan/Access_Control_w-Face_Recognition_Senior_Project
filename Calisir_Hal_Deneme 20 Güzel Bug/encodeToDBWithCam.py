import cv2
from tkinter import *
import tkinter.simpledialog
import numpy as np
import os
import psycopg2
import psycopg2.extras
import face_recognition
from PIL import Image, ImageTk


class App:
    def __init__(self, window, window_title, video_source=1):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH),
                             height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # Entry widget
        self.entry_var = StringVar()
        self.entry = Entry(window, textvariable=self.entry_var)
        self.entry.pack()
        self.entry_var.trace_add('write', self.activate_button)

        # Button that lets the user take a snapshot
        self.btn_snapshot = Button(window, text="Save", width=50, command=self.save_face, state='disabled')
        self.btn_snapshot.pack(anchor=CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update_frame()

        self.window.mainloop()

    def update_frame(self):
        ret, frame = self.vid.read()
        if ret:
            self.current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.current_frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

        self.window.after(self.delay, self.update_frame)

    def save_face(self):
        # save frame and name
        self.saved_frame = self.current_frame
        self.saved_name = self.entry_var.get()

        # Create second window
        self.window2 = Toplevel()
        self.window2.title("Confirm Save")

        # Display image in the second window
        self.photo2 = ImageTk.PhotoImage(image=Image.fromarray(self.saved_frame))
        self.canvas2 = Canvas(self.window2, width=self.saved_frame.shape[1], height=self.saved_frame.shape[0])
        self.canvas2.create_image(0, 0, image=self.photo2, anchor=NW)
        self.canvas2.pack()

        # Display name in the second window
        self.entry2_var = StringVar(value=self.saved_name)
        self.entry2 = Entry(self.window2, textvariable=self.entry2_var)
        self.entry2.pack()

        # Confirm and Cancel buttons
        self.btn_confirm = Button(self.window2, text="Confirm", command=self.save_to_database)
        self.btn_confirm.pack()
        self.btn_cancel = Button(self.window2, text="Cancel", command=self.window2.destroy)
        self.btn_cancel.pack()

    def activate_button(self, *args):
        if self.entry_var.get():
            self.btn_snapshot['state'] = 'normal'
        else:
            self.btn_snapshot['state'] = 'disabled'

    def save_to_database(self):
        # Your PostgreSQL connection code and face encoding code here
        face_image = self.saved_frame
        face_encodings = face_recognition.face_encodings(face_image)

        if len(face_encodings) > 0:
            face_encoding = face_encodings[0]
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
                        create_script = ''' CREATE TABLE IF NOT EXISTS faces (
                                                            id SERIAL PRIMARY KEY,
                                                            name    varchar(100) NOT NULL,
                                                            encoding BYTEA )'''
                        cur.execute(create_script)
                        insert_script = 'INSERT INTO faces (name, encoding) VALUES (%s, %s)'
                        cur.execute(insert_script, (self.entry2_var.get(), face_encoding_bytes))
            except Exception as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()

            self.window2.destroy()


if __name__ == '__main__':
    App(Tk(), "Face Save App")
