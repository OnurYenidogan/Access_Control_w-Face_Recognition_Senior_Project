import tkinter as tk
import threading

class ChildWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Child Window")

class MainApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.open_window_button = tk.Button(self, text="Open Window", command=self.open_window)
        self.open_window_button.pack()

    def open_window(self):
        window = ChildWindow(self.master)
        window_thread = threading.Thread(target=window.mainloop)
        window_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(master=root)
    app.pack()
    app.mainloop()
