import tkinter as tk
import subprocess


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.start_button = tk.Button(self, text="Giriş-Çıkış Başlat", command=self.start_process)
        self.start_button.grid(row=0, column=0)

    def start_process(self):
        self.process_window = tk.Toplevel(self.master)
        self.process_window.title("Giriş-Çıkış Seçenekleri")

        self.camera_label = tk.Label(self.process_window, text="Kamera Seçimi:")
        self.camera_label.grid(row=0, column=0)

        self.camera_list = ["Kamera 1", "Kamera 2", "Kamera 3"]  # örnek olarak kameralar listeleniyor
        self.selected_camera = tk.StringVar()
        self.selected_camera.set(self.camera_list[0])
        for i, camera in enumerate(self.camera_list):
            self.camera_button = tk.Radiobutton(self.process_window, text=camera, variable=self.selected_camera,
                                                value=camera)
            self.camera_button.grid(row=1 + i, column=0)

        self.option_label = tk.Label(self.process_window, text="Seçiminiz:")
        self.option_label.grid(row=len(self.camera_list) + 1, column=0)

        self.selected_option = tk.StringVar()
        self.selected_option.set("Giriş")  # örnek olarak başlangıçta "Giriş" seçeneği seçili

        self.option_button1 = tk.Radiobutton(self.process_window, text="Giriş", variable=self.selected_option,
                                             value="Giriş")
        self.option_button1.grid(row=len(self.camera_list) + 2, column=0)

        self.option_button2 = tk.Radiobutton(self.process_window, text="Çıkış", variable=self.selected_option,
                                             value="Çıkış")
        self.option_button2.grid(row=len(self.camera_list) + 3, column=0)

        self.start_button2 = tk.Button(self.process_window, text="Başlat", command=self.start_function)
        self.start_button2.grid(row=len(self.camera_list) + 4, column=0)

    def start_function(self):
        print("Seçilen Kamera:", self.selected_camera.get())
        print("Seçilen Seçenek:", self.selected_option.get())


root = tk.Tk()
app = Application(master=root)
app.mainloop()
