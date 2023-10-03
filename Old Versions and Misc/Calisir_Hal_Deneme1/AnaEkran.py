import tkinter as tk
import threading
from tkinter import messagebox

window = tk.Tk()
window.title("Başlık")
window.geometry("300x150")


def run_kamera_sec():
    import subprocess
    subprocess.run(["python", "kameraSec.py"])


def run_kamera_sec_thread():
    t = threading.Thread(target=run_kamera_sec)
    t.start()


kameraSec = tk.Button(window, text="Giriş-Çıkış Başlat", command=run_kamera_sec_thread)
kameraSec.pack(pady=10)


def run_123():
    import subprocess
    subprocess.run(["python", "123.py"])


def run_123_thread():
    t = threading.Thread(target=run_123)
    t.start()


button123 = tk.Button(window, text="123 çalıştır", command=run_123_thread)
button123.pack(pady=10)

window.mainloop()
