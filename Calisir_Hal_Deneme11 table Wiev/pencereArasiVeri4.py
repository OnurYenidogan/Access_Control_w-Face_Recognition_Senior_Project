import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from some_functions import get_camera_list, get_known_faces_from_db, DBconn
import subprocess
import os
import sys
import psycopg2
from tkinter import filedialog

global pgConn
pgConn = DBconn()




class AddFaceWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Yüz Ekle")

        # Toplu ekle butonu
        self.batch_button = tk.Button(
            self.master,
            text="Toplu Ekle",
            command=self.batch_add_faces
        )
        self.batch_button.pack()



    def batch_add_faces(self):
        """        folder_path = filedialog.askdirectory()
        print(folder_path)"""
        subprocess.Popen(['python', os.path.join(sys.path[0], 'encodeToDB.py')])







class ShowTableWindow:
    def __init__(self, master):
        self.master = master
        #self.master.title(f"{db_name} Veritabanı - {table_name} Tablosu")

        # PostgreSQL veritabanına bağlanma işlemi
        conn = pgConn

        # Tablo verilerini çeken sorgu
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM faces")

        # Tablo verilerini Tkinter grid widget'ı üzerinde gösterme işlemi
        rows = cur.fetchall()
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                label = tk.Label(self.master, text=value)
                label.grid(row=i, column=j, padx=5, pady=5)

        # Bağlantıyı kapatma işlemi
        cur.close()
        conn.close()



class CameraSelect:
    def __init__(self, master):
        self.master = master
        self.master.title("Kamera Seçimi")

        self.BagliCams = get_camera_list()

        self.camera_type = tk.StringVar()
        self.camera_type.set("TypeA")

        # Kamera türü seçimi için radio butonlar
        self.typea_radio = ttk.Radiobutton(self.master, text="Giriş", variable=self.camera_type, value="TypeA")
        self.typea_radio.grid(row=0, column=0, padx=5, pady=5)

        self.typeb_radio = ttk.Radiobutton(self.master, text="Çıkış", variable=self.camera_type, value="TypeB")
        self.typeb_radio.grid(row=1, column=0, padx=5, pady=5)

        # Kamera listesi için dropdown
        self.camera_list = ttk.Combobox(self.master, values=self.BagliCams)
        self.camera_list.grid(row=2, column=0, padx=5, pady=5)

        # Seçimi onaylamak için buton
        self.confirm_button = ttk.Button(self.master, text="Kamera Başlat", command=self.cameraStart)
        self.confirm_button.grid(row=3, column=0, padx=5, pady=5)

    def cameraStart(self):

        print(self.camera_list.get())
        CameraWindowIn_Out.recognation(self, self.camera_list.get(), self.camera_type.get())



class CameraWindowIn_Out:
    def __init__(self, master, person_list, cam_No):
        self.master = master
        self.master.title("Cam"+cam_No+" In")
        self.person_list = person_list
        self.cam_No = cam_No
        print(cam_No)
        self.listbox = tk.Listbox(self.master)
        for person in person_list:
            self.listbox.insert(tk.END, person)
        self.listbox.pack()
        self.button = tk.Button(self.master, text="Kişi Ekle", command=self.add_person_window)
        self.button.pack()
        self.camera_label = tk.Label(self.master)
        self.camera_label.pack()

    def recognation(self, cam_No, CType):
        db_file = os.path.join(sys.path[0], 'recognitionDB-In-Out.py')
        subprocess.Popen(['python', db_file, cam_No, CType])


def open_CameraSelect():
    global camSelect
    camSelect = CameraSelect(tk.Toplevel())


def main():
    global root
    root = tk.Tk()
    root.title("Ana Pencere")
    start_button = tk.Button(root, text="Kamerayı Başlat", command=open_CameraSelect)
    start_button.pack()
    add_button = tk.Button(root, text="Yoklama", command=lambda: ShowTableWindow(tk.Toplevel()))
    add_button.pack()
    add_button = tk.Button(root, text="Kişi Ekle", command=lambda: AddFaceWindow(tk.Toplevel()))
    add_button.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
