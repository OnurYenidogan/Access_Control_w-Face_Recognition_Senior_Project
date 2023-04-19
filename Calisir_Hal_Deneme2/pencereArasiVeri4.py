import cv2
import tkinter as tk
from PIL import Image, ImageTk

# örnek bir kişi listesi
person_list = ["John Doe", "Jane Smith", "Bob Johnson"]

def update_person_list(new_person):
    person_list.append(new_person)
    print("Kişi listesi güncellendi:", person_list)
    # kamera penceresindeki kişi listesini güncelle
    if cam_window:
        cam_window.update_list(person_list)

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
            self.listbox.insert(tk.END, person)
        self.listbox.pack()
        self.button = tk.Button(self.master, text="Kişi Ekle", command=self.add_person_window)
        self.button.pack()
        self.camera_label = tk.Label(self.master)
        self.camera_label.pack()

        # OpenCV ile kamera akışını al
        self.cap = cv2.VideoCapture(0)
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

def open_camera_window():
    global cam_window
    cam_window = CameraWindow(tk.Toplevel(), person_list)

def main():
    global root
    root = tk.Tk()
    root.title("Ana Pencere")
    start_button = tk.Button(root, text="Kamerayı Başlat", command=open_camera_window)
    start_button.pack()
    add_button = tk.Button(root, text="Kişi Ekle", command=lambda: AddPersonWindow(tk.Toplevel()))
    add_button.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
