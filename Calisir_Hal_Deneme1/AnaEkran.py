import tkinter as tk
import threading
from tkinter import messagebox

window = tk.Tk()
window.title("Asd ve 123")
window.geometry("300x150")


def run_asd():
    import subprocess
    subprocess.run(["python", "kameraSec.py"])


def run_asd_thread():
    t = threading.Thread(target=run_asd)
    t.start()


kameraSec = tk.Button(window, text="kameraSec", command=run_asd_thread)
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
