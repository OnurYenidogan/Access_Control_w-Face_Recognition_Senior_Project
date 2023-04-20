import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from some_functions import get_camera_list, get_known_faces_from_db

# örnek bir kişi listesi
person_list = ["John Doe", "Jane Smith", "Bob Johnson"]

def update_person_list(new_person):
    person_list.append(new_person)
    print("Kişi listesi güncellendi:", person_list)
    # kamera penceresindeki kişi listesini güncelle
    if camSelect:
        camSelect.update_list(person_list)

def PostgreSQL_Connection():
        print()

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
        self.typea_radio = ttk.Radiobutton(self.master, text="TypeA", variable=self.camera_type, value="TypeA")
        self.typea_radio.grid(row=0, column=0, padx=5, pady=5)

        self.typeb_radio = ttk.Radiobutton(self.master, text="TypeB", variable=self.camera_type, value="TypeB")
        self.typeb_radio.grid(row=1, column=0, padx=5, pady=5)

        # Kamera listesi için dropdown
        self.camera_list = ttk.Combobox(self.master, values=self.BagliCams)
        self.camera_list.grid(row=2, column=0, padx=5, pady=5)

        # Seçimi onaylamak için buton
        self.confirm_button = ttk.Button(self.master, text="Kamera Başlat", command=self.cameraStart)
        self.confirm_button.grid(row=3, column=0, padx=5, pady=5)

    def cameraStart(self):
        if self.camera_type.get() == "TypeA":
            CameraWindow(tk.Toplevel(), person_list, self.camera_list.get())
        else:
            CameraWindow(tk.Toplevel(), person_list, self.camera_list.get())



        # burada bir hata mesajı yazdırabilirsiniz


class CameraWindow:
    def __init__(self, master, person_list, cam_No):
        self.master = master
        self.master.title("Cam"+cam_No)
        self.person_list = person_list
        self.listbox = tk.Listbox(self.master)
        for person in person_list:
            self.listbox.insert(tk.END, person)
        self.listbox.pack()
        self.button = tk.Button(self.master, text="Kişi Ekle", command=self.add_person_window)
        self.button.pack()
        self.camera_label = tk.Label(self.master)
        self.camera_label.pack()

        # OpenCV ile kamera akışını al
        self.cap = cv2.VideoCapture(int(cam_No))

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.show_frame()

    def show_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # OpenCV BGR formatından PIL Image formatına dönüştür
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)
        self.camera_label.after(10, self.show_frame)

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
