import tkinter as tk


class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Ana Pencere")

        self.start_button = tk.Button(self.root, text="Kamerayı Başlat", command=self.open_window)
        self.start_button.pack()

        self.persons_list = ["Person 1", "Person 2", "Person 3"]
        self.persons_label = tk.Label(self.root, text="\n".join(self.persons_list))
        self.persons_label.pack()

    def open_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Yeni Pencere")

        self.add_person_button = tk.Button(self.new_window, text="Kişi Ekle", command=self.add_person_window)
        self.add_person_button.pack()

        # burada kamera akışı ve yüz tanıma işlemleri olacak

    def add_person_window(self):
        self.add_person_window = tk.Toplevel(self.new_window)
        self.add_person_window.title("Kişi Ekleme Penceresi")

        self.add_person_label = tk.Label(self.add_person_window, text="Yeni kişinin ismini girin:")
        self.add_person_label.pack()

        self.add_person_entry = tk.Entry(self.add_person_window)
        self.add_person_entry.pack()

        self.add_person_button = tk.Button(self.add_person_window, text="Ekle", command=self.add_person)
        self.add_person_button.pack()

    def add_person(self):
        new_person_name = self.add_person_entry.get()
        if new_person_name != "":
            self.persons_list.append(new_person_name)
            self.persons_label.config(text="\n".join(self.persons_list))
        self.add_person_window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
