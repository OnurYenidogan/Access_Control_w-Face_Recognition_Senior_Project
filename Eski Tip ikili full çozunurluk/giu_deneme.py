import os
import sys
import subprocess
import tkinter as tk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Ana Pencere")
        self.attributes('-fullscreen', False)
        self.resizable(True, True)

        button = tk.Button(self, text="Diğer Pencereyi Aç", command=self.open_new_window)
        button.pack(pady=20)

    def open_new_window(self):
        # Bu dosya ile aynı dizindeki recognitionDB.py dosyasının yolunu belirtin
        db_file = os.path.join(sys.path[0], 'recognitionDB.py')
        subprocess.Popen(['python', db_file])
        db_file2 = os.path.join(sys.path[0], 'recognitionDB2.py')
        subprocess.Popen(['python', db_file2])


if __name__ == '__main__':
    window = MainWindow()
    window.mainloop()
