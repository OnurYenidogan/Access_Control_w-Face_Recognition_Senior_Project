import tkinter as tk
import threading
from some_functions import get_camera_list, get_known_faces_from_db, DBconn
from CamFaceRecoDB import camReco

global cam_i
cam_i = -1
global cams
cams = []
global pgConn
pgConn = DBconn('localhost', 'SeniorProject', 'postgres', '1234', 5432)

class MainApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.open_window_button = tk.Button(self, text="Open Window", command=self.open_new_window)
        self.open_window_button.pack()

    def open_new_window(self):
        global cam_i
        # Yeni pencere oluştur
        new_window = tk.Toplevel(root)
        new_window.title("New Window")
        cam_i += 1
        cams.append(camReco(get_known_faces_from_db(pgConn), cam_i, pgConn))
        # Yeni pencerede fonksiyonu başlat
        cams[cam_i].run()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(master=root)
    app.pack()
    root.mainloop()
