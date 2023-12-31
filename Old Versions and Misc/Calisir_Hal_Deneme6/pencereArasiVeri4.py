import tkinter as tk
from tkinter import ttk
from some_functions import get_camera_list, get_known_faces_from_db, DBconn
import subprocess
import os
import sys
import multiprocessing
from recognitionDB_In import face_confidence,camReco
import cv2


# örnek bir kişi listesi
global pgConn
pgConn = DBconn('localhost', 'SeniorProject', 'postgres', '1234', 5432)
global person_list
person_list=get_known_faces_from_db(pgConn)
def update_person_list(new_person):
    person_list.append(new_person)
    print("Kişi listesi güncellendi:", person_list)
    # kamera penceresindeki kişi listesini güncelle
    if camSelect:
        camSelect.update_list(person_list)
UsedCams=set()

class AddPersonWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Kişi Ekle")
        self.label = tk.Label(self.master, text="Yeni Kişi Adı:")
        self.label.pack()
        self.entry = tk.Entry(self.master)
        self.entry.pack()
        self.button = tk.Button(self.master, text="Ekle", command=self.add_person)
        self.button.pack()

    def add_person(self):
        new_person = self.entry.get()
        update_person_list(new_person)
        self.master.destroy()

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
        UsedCams.add(self.camera_list.get())
        print(UsedCams)
        if self.camera_type.get() == "TypeA":
            CameraWindowIn(tk.Toplevel(), person_list, self.camera_list.get(),'In')
            CameraWindowIn.recognation(self)
        else:
            CameraWindowOut(tk.Toplevel(), person_list, self.camera_list.get())
            CameraWindowOut.recognation(self)



        # burada bir hata mesajı yazdırabilirsiniz


class CameraWindowIn:
    def __init__(self, master, person_list, cam_No, cam_Type):
        self.master = master
        self.master.title("Cam"+cam_No+" In")
        #self.person_list = person_list
        self.listbox = tk.Listbox(self.master)
        for person in person_list:
            self.listbox.insert(tk.END, person)
        self.listbox.pack()
        self.button = tk.Button(self.master, text="Kişi Ekle", command=self.add_person_window)
        self.button.pack()
        self.camera_label = tk.Label(self.master)
        self.camera_label.pack()

    def recognation(self):
        """db_file = os.path.join(sys.path[0], 'recognitionDB_In.py')
        subprocess.Popen(['python', db_file])"""
        camReco(person_list,1,pgConn)


    def update_list(self, person_list):
        self.person_list = person_list
        self.listbox.delete(0, tk.END)
        for person in person_list:
            self.listbox.insert(tk.END, person)

    def add_person_window(self):
        AddPersonWindow(tk.Toplevel())

class CameraWindowOut:
    def __init__(self, master, person_list, cam_No):
        self.master = master
        self.master.title("Cam"+cam_No+" Out")
        self.person_list = person_list
        self.listbox = tk.Listbox(self.master)
        for person in person_list:
            self.listbox.insert(tk.END, person)
        self.listbox.pack()
        self.button = tk.Button(self.master, text="Kişi Ekle", command=self.add_person_window)
        self.button.pack()
        self.camera_label = tk.Label(self.master)
        self.camera_label.pack()

    def recognation(self):
        db_file = os.path.join(sys.path[0], 'recognitionDB-Out.py')
        subprocess.Popen(['python', db_file])

    def update_list(self, person_list):
        self.person_list = person_list
        self.listbox.delete(0, tk.END)
        for person in person_list:
            self.listbox.insert(tk.END, person)

    def add_person_window(self):
        AddPersonWindow(tk.Toplevel())


def open_CameraSelect():
    global camSelect
    camSelect = CameraSelect(tk.Toplevel())


def main():
    global root
    root = tk.Tk()
    root.title("Ana Pencere")
    start_button = tk.Button(root, text="Kamerayı Başlat", command=open_CameraSelect)
    start_button.pack()
    add_button = tk.Button(root, text="Kişi Ekle", command=lambda: AddPersonWindow(tk.Toplevel()))
    add_button.pack()
    root.mainloop()

if __name__ == "__main__":

    main()
