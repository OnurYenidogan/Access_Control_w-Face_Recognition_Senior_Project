import tkinter as tk
from tkinter import ttk

class CameraSelect:
    def __init__(self, master):
        self.master = master
        self.master.title("Kamera Seçimi")

        self.camera_type = tk.StringVar()
        self.camera_type.set("TypeA")

        # Kamera türü seçimi için radio butonlar
        self.typea_radio = ttk.Radiobutton(self.master, text="TypeA", variable=self.camera_type, value="TypeA")
        self.typea_radio.grid(row=0, column=0, padx=5, pady=5)

        self.typeb_radio = ttk.Radiobutton(self.master, text="TypeB", variable=self.camera_type, value="TypeB")
        self.typeb_radio.grid(row=1, column=0, padx=5, pady=5)

        # Kamera listesi için dropdown
        self.camera_list = ttk.Combobox(self.master, values=["Camera 1", "Camera 2", "Camera 3"])
        self.camera_list.grid(row=2, column=0, padx=5, pady=5)

        # Seçimi onaylamak için buton
        self.confirm_button = ttk.Button(self.master, text="Onayla", command=self.confirm_selection)
        self.confirm_button.grid(row=3, column=0, padx=5, pady=5)

    def confirm_selection(self):
        print("Seçilen kamera türü:", self.camera_type.get())
        print("Seçilen kamera:", self.camera_list.get())

root = tk.Tk()
app = CameraSelect(root)
root.mainloop()
