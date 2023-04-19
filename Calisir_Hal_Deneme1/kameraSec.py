import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk


class KameraSec:

    def __init__(self, root):
        self.root = root
        self.root.title("Kamera Seç")
        self.root.geometry("640x480")

        self.kameralar = self.list_kameralar()
        self.kamera_secim = tk.StringVar()
        self.kamera_secim.set(self.kameralar[0])
        self.dropdown = ttk.Combobox(self.root, values=self.kameralar, textvariable=self.kamera_secim)
        self.dropdown.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Başlat", command=self.baslat)
        self.start_button.pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.pack()

        self.root.bind('<Escape>', lambda e: self.root.quit())  # ESC tuşuna basıldığında çıkış yap

    def list_kameralar(self):
        kamera_listesi = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.read()[0]:
                kamera_listesi.append(f"Kamera {i}")
            cap.release()
        return kamera_listesi

    def baslat(self):
        self.dropdown.config(state="disabled")
        self.start_button.config(state="disabled")

        self.cap = cv2.VideoCapture(int(self.kamera_secim.get().split()[-1]))
        self.show_frame()

    def show_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(img)
            self.canvas.config(width=self.root.winfo_width(), height=self.root.winfo_height())
            self.canvas.create_image(0, 0, image=img_tk, anchor='nw')
            self.canvas.img_tk = img_tk
            self.root.after(10, self.show_frame)
        else:
            self.cap.release()
            self.dropdown.config(state="normal")
            self.start_button.config(state="normal")


if __name__ == '__main__':
    root = tk.Tk()
    kamera_sec = KameraSec(root)
    root.mainloop()
