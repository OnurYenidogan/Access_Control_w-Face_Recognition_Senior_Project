import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class KameraSec:

    def __init__(self, root):
        self.root = root
        self.root.title("Kamera Seç")
        self.root.geometry("600x400")

        self.cap = None
        self.video_frame = tk.Label(self.root)
        self.camera_select = ttk.Combobox(self.root, values=self.get_camera_list(), state="readonly")
        self.camera_select.current(0)
        self.start_button = tk.Button(self.root, text="Başlat", command=self.start_video)

        self.camera_select.pack(pady=10)
        self.start_button.pack(pady=10)
        self.video_frame.pack()

        self.root.bind("<Configure>", self.resize_video)

    def get_camera_list(self):
        camera_list = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.read()[0]:
                camera_list.append(f"Kamera {i}")
            cap.release()
        return camera_list

    def start_video(self):
        selected_camera_index = int(self.camera_select.get().split()[-1])
        self.cap = cv2.VideoCapture(selected_camera_index)
        self.show_video()

    def show_video(self):
        ret, frame = self.cap.read()
        if ret:
            # Resize the frame to fit in the window
            frame = cv2.resize(frame, (self.root.winfo_width(), self.root.winfo_height()))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = tk.PhotoImage(width=frame.shape[1], height=frame.shape[0])
            img = self.convert_frame_to_photoimage(frame, img)
            self.video_frame.config(image=img)
            self.video_frame.image = img
            self.video_frame.after(10, self.show_video)

    def convert_frame_to_photoimage(self, frame, img):
        photo = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(photo)
        return photo

    def resize_video(self, event):
        if self.cap is not None:
            _, frame = self.cap.read()
            frame = cv2.resize(frame, (event.width, event.height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = tk.PhotoImage(width=frame.shape[1], height=frame.shape[0])
            img = self.convert_frame_to_photoimage(frame, img)
            self.video_frame.config(image=img)
            self.video_frame.image = img

root = tk.Tk()
KameraSec(root)
root.mainloop()
