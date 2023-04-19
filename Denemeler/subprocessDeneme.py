import tkinter as tk
import subprocess


class App:
    def __init__(self, master):
        self.master = master
        self.count = 0

        # Ana pencereyi oluşturun
        self.label = tk.Label(master, text="Count: {}".format(self.count))
        self.label.pack()

        # Düğmeyi oluşturun
        button = tk.Button(master, text="Click Me!", command=self.run_subprocess)
        button.pack()

        # Yeni pencereyi oluşturun
        self.new_window = tk.Toplevel(master)
        self.new_label = tk.Label(self.new_window, text="New Window")
        self.new_label.pack()

    def run_subprocess(self):
        # Sayacı arttırın
        self.count += 1
        self.label.config(text="Count: {}".format(self.count))

        # Yeni pencereyi güncelleyin
        self.new_label.config(text="Count: {}".format(self.count))

        # Subprocess'i çalıştırın
        subprocess.Popen(["python", "-c", "print('Hello World')"])


root = tk.Tk()
app = App(root)
root.mainloop()
