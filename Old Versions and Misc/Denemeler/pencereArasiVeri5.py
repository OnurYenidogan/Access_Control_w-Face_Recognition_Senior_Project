import tkinter as tk
import cv2
import numpy as np

# örnek bir kişi listesi
person_list = ["John Doe", "Jane Smith", "Bob Johnson"]

def update_person_list(new_person):
    person_list.append(new_person)
    print("Kişi listesi güncellendi:", person_list)
    # kamera penceresindeki kişi listesini güncelle
    if cam_window:
        cam_window.update_list(person_list)

class CameraSettingsWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Kamera Ayarları")
        self.camera_type_var = tk.StringVar(value="giriş")
        self.camera_type_label = tk.Label(self.master, text="Kamera Türü:")
        self.camera_type_label.pack()
        self.camera_type_frame = tk.Frame(self.master)
        self.input_radio = tk.Radiobutton(self.camera_type_frame, text="Giriş", variable=self.camera_type_var, value="giriş")
        self.input_radio.pack(side=tk.LEFT)
        self.output_radio = tk.Radiobutton(self.camera_type_frame, text="Çıkış", variable=self.camera_type_var, value="çıkış")
        self.output_radio.pack(side=tk.LEFT)
        self.camera_type_frame.pack()
        self.camera_dropdown_label = tk.Label(self.master, text="Kamera Seçin:")
        self.camera_dropdown_label.pack()
        self.camera_dropdown = tk.OptionMenu(self.master, tk.StringVar(), *range(10))
        self.camera_dropdown.pack()
        self.start_button = tk.Button(self.master, text="Başlat", command=self.start_camera)
        self.start_button.pack()

    def start_camera(self):
        camera_number = int(self.camera_dropdown.var.get())
        camera_type = self.camera_type_var.get()
        print("Kamera Başlatılıyor...")
        cap = cv2.VideoCapture(camera_number + cv2.CAP_DSHOW)
        if camera_type == "çıkış":
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
        while True:
            ret, frame = cap.read()
            if ret:
                if camera_type == "giriş":
                    cv2.imshow('frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                elif camera_type == "çıkış":
                    out.write(frame)
            else:
                break
        cap.release()
        if camera_type == "çıkış":
            out.release()
        cv2.destroyAllWindows()

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

class CameraWindow:
    def __init__(self, master, person_list):
        self.master = master
        self.master.title("Kamera Akışı")
        self.person_list = person_list
        self.listbox = tk.Listbox(self.master)
        for person in person_list:
            self.listbox.insert
