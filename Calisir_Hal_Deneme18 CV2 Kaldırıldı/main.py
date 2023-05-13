import tkinter as tk
from tkinter import ttk
from some_functions import get_camera_list, DBconn, DBconnCheck
import subprocess
import os
import sys
import pandas as pd
from tkinter import filedialog
from datetime import datetime
import configparser
from tkinter import messagebox

"""Gereksiz olanlar projeden kaldırılmadığı için burada yazıyor"""

"""global pgConn
pgConn = DBconn()"""


def batch_add_faces():
    """        folder_path = filedialog.askdirectory()
    print(folder_path)"""
    subprocess.Popen(['python', os.path.join(sys.path[0], 'encodeToDB.py')])


class AddFaceWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Yüz Ekle")

        # Toplu ekle butonu
        self.batch_button = tk.Button(
            self.master,
            text="Toplu Ekle",
            command=self.batch_add_faces
        )
        self.batch_button.pack()

    def batch_add_faces(self):
        """        folder_path = filedialog.askdirectory()
        print(folder_path)"""
        subprocess.Popen(['python', os.path.join(sys.path[0], 'encodeToDB.py')])


import tkinter as tk
from tkinter import ttk

class ShowTableWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Yoklama Tablosu")

        # PostgreSQL veritabanına bağlanma işlemi
        conn = DBconn()
        print(conn)

        # Tablo verilerini çeken sorgu
        cur = conn.cursor()
        cur.execute(f"SELECT id, name, status, last_reco FROM faces;")

        # Tablo verilerini bir DataFrame'e aktarma işlemi
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=["ID", "İsim", "Durum", "Son Tanıma Tarihi"])
        df["Durum"] = df["Durum"].apply(lambda x: "İçeride" if x == "i" else "Dışarıda")

        # Bağlantıyı kapatma işlemi
        cur.close()
        conn.close()

        # DataFrame'i Excel dosyasına kaydetme işlemi
        save_file_path = filedialog.askdirectory()
        if save_file_path:
            datetime_str = datetime.now().strftime("%d-%m-%Y %H.%M.%S") + " Yoklaması"
            df.to_excel(save_file_path + f"/{datetime_str}.xlsx", sheet_name="Yoklama", index=False)

        # Treeview widget'ını oluşturma işlemi
        tree = ttk.Treeview(self.master)
        tree["columns"]=("ID", "İsim", "Durum", "Son Tanıma Tarihi")

        # Her bir sütun için başlık ve genişlik belirleme
        for column in tree["columns"]:
            tree.column(column, width=100)
            tree.heading(column, text=column)

        # DataFrame'deki verileri Treeview widget'ına ekleme
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack()



class CameraSelect:
    def __init__(self, master):
        self.master = master
        self.master.title("Kamera Seçimi")
        self.master.configure(background='#F5F5F5')

        self.BagliCams = get_camera_list()

        self.camera_type = tk.StringVar(value="TypeA")

        # Kamera türü seçimi için radio butonlar
        self.typea_radio = ttk.Radiobutton(self.master, text="Giriş", variable=self.camera_type, value="TypeA")
        self.typea_radio.grid(row=0, column=0, padx=10, pady=10)

        self.typeb_radio = ttk.Radiobutton(self.master, text="Çıkış", variable=self.camera_type, value="TypeB")
        self.typeb_radio.grid(row=0, column=1, padx=10, pady=10)

        # Kamera listesi için dropdown
        self.camera_list = ttk.Combobox(self.master, values=[f"Kamera {cam}" for cam in self.BagliCams],
                                        state='readonly', width=20)
        self.camera_list.current(0)
        self.camera_list.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Seçimi onaylamak için buton
        self.confirm_button = ttk.Button(self.master, text="Kamera Başlat", command=self.cameraStart)
        self.confirm_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="s")
        self.confirm_button.configure(style='AccentButton.TButton')
        self.master.bind("<Return>", lambda event: self.cameraStart())

    def cameraStart(self):
        camera_number_str = self.camera_list.get().split("Kamera ")[1]
        cmrNo = int(camera_number_str)
        CameraWindowIn_Out.recognation(self, cmrNo, self.camera_type.get())

    def cameraStart(self):
        print(self.camera_list.get())
        camera_number_str = self.camera_list.get().split("Kamera ")[1]
        print(camera_number_str)
        CameraWindowIn_Out.recognation(self, camera_number_str, self.camera_type.get())


class CameraWindowIn_Out:
    def __init__(self, master, person_list, cam_No):
        self.master = master
        self.master.title("Cam" + cam_No + " In")
        self.person_list = person_list
        self.cam_No = cam_No
        print(cam_No)
        self.listbox = tk.Listbox(self.master)
        for person in person_list:
            self.listbox.insert(tk.END, person)
        self.listbox.pack()
        self.button = tk.Button(self.master, text="Kişi Ekle", command=self.add_person_window)
        self.button.pack()
        self.camera_label = tk.Label(self.master)
        self.camera_label.pack()

    def recognation(self, cam_No, CType):
        db_file = os.path.join(sys.path[0], 'recognitionDB-In-Out.py')
        subprocess.Popen(['python', db_file, cam_No, CType])


def open_CameraSelect():
    global camSelect
    camSelect = CameraSelect(tk.Toplevel())


def main():
    # Stil ayarları
    BG_COLOR = "#F0F0F0"
    LABEL_COLOR = "#333333"
    ENTRY_WIDTH = 30
    ENTRY_HEIGHT = 2
    BUTTON_COLOR = "#4287f5"
    BUTTON_TEXT_COLOR = "#FFFFFF"

    config = configparser.ConfigParser()

    def show_form_dialog():

        ini_tk = tk.Tk()
        ini_tk.title("VT bilgilerini girin")
        ini_tk.withdraw(
                        "Lütfen PostgreSQL bağlantısı için gerekli bilgileri giriniz. "
                        "Bu işlem config.ini dosyası varsa üstüne yeni bilgileri kaydedecektir, "
                        "yoksa yeni bir dosya oluşturacaktır.")
        dialog = tk.Toplevel(ini_tk)

        def on_dialog_close():
            dialog.destroy()
            sys.exit()

        dialog.protocol("WM_DELETE_WINDOW", on_dialog_close)  # Çarpıya basılınca formu kapat ve programı sonlandır

        dialog.configure(bg=BG_COLOR)

        def create_entry_field(label_text):
            frame = tk.Frame(dialog, bg=BG_COLOR)
            frame.pack(pady=5)
            label = tk.Label(frame, text=label_text, bg=BG_COLOR, fg=LABEL_COLOR)
            label.pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=ENTRY_WIDTH)
            entry.pack(side=tk.LEFT)
            return entry

        def validate_form():
            hostname = hostname_entry.get()
            database = database_entry.get()
            username = username_entry.get()
            pwd = pwd_entry.get()
            port_id = port_id_entry.get()

            if not (hostname and database and username and pwd and port_id):
                messagebox.showwarning("Uyarı", "Lütfen bütün bilgileri giriniz.")
            else:
                dialog.quit()

        hostname_entry = create_entry_field("Hostname:")
        database_entry = create_entry_field("Database:")
        username_entry = create_entry_field("Username:")
        pwd_entry = create_entry_field("Password:")
        port_id_entry = create_entry_field("Port ID:")

        ok_button = tk.Button(dialog, text="OK", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=validate_form)
        ok_button.pack(pady=10)

        dialog.mainloop()

        if dialog.winfo_exists():
            hostname = hostname_entry.get()
            database = database_entry.get()
            username = username_entry.get()
            pwd = pwd_entry.get()
            port_id = port_id_entry.get()

            ini_tk.destroy()

            return hostname, database, username, pwd, port_id
        else:
            sys.exit()

    if os.path.exists('config.ini'):
        config.read('config.ini')
        print(dict(config['Database']))  # debug
        conn = DBconnCheck(
            config['Database']['hostname'],
            config['Database']['database'],
            config['Database']['username'],
            config['Database']['pwd'],
            config['Database']['port_id']
        )
        if conn is None:
            os.remove('config.ini')
            form_data = show_form_dialog()
            while form_data is None:
                form_data = show_form_dialog()
            hostname, database, username, pwd, port_id = form_data
        else:
            # Veritabanı bağlantısı başarılı, devam edilebilir.
            pass
    else:
        form_data = show_form_dialog()
        while form_data is None:
            form_data = show_form_dialog()
        hostname, database, username, pwd, port_id = form_data

        conn = DBconnCheck(hostname, database, username, pwd, port_id)

        while conn is None:
            form_data = show_form_dialog()
            while form_data is None:
                form_data = show_form_dialog()
            hostname, database, username, pwd, port_id = form_data

        config['Database'] = {
            'hostname': hostname,
            'database': database,
            'username': username,
            'pwd': pwd,
            'port_id': port_id
        }

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    global root
    root = tk.Tk()
    root.title("Ana Pencere")

    start_button = tk.Button(root, text="Kamerayı Başlat", command=open_CameraSelect,
                             width=20, height=2, bg="blue", fg="white", font=("Helvetica", 16))
    start_button.pack(padx=10, pady=10)

    add_button1 = tk.Button(root, text="Yoklama", command=lambda: ShowTableWindow(tk.Toplevel()),
                            width=20, height=2, bg="green", fg="white", font=("Helvetica", 16))
    add_button1.pack(padx=10, pady=10)

    add_button2 = tk.Button(root, text="Kişi Ekle", command=batch_add_faces,
                            width=20, height=2, bg="red", fg="white", font=("Helvetica", 16))
    add_button2.pack(padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
