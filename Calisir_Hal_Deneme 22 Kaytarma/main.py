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




from tkinter import ttk
import tkinter as tk

class PresenceCalculatorWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("İçeride Kalma Süresi Hesaplama")

        # PostgreSQL veritabanına bağlanma işlemi
        self.conn = DBconn()

        # Kişi isimlerini çeken sorgu
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT id, name FROM faces;")
        self.ids = [(id[0], id[1]) for id in self.cur.fetchall()]

        # Kullanıcı arayüz elemanları oluşturma
        self.id_label = ttk.Label(master, text="ID")
        self.id_label.pack()
        self.id_var = tk.StringVar()
        self.id_dropdown = ttk.Combobox(master, textvariable=self.id_var, values=[id[1] for id in self.ids])
        self.id_dropdown.pack()

        self.start_datetime_label = ttk.Label(master, text="Başlangıç Tarih ve Saati (YYYY-MM-DD HH:MI:SS)")
        self.start_datetime_label.pack()
        self.start_datetime_entry = ttk.Entry(master)
        self.start_datetime_entry.pack()

        self.end_datetime_label = ttk.Label(master, text="Bitiş Tarih ve Saati (YYYY-MM-DD HH:MI:SS)")
        self.end_datetime_label.pack()
        self.end_datetime_entry = ttk.Entry(master)
        self.end_datetime_entry.pack()

        self.calculate_button = ttk.Button(master, text="Hesapla", command=self.calculate_presence)
        self.calculate_button.pack()

        # Tablo oluşturma
        self.tree = ttk.Treeview(master, columns=('ID', 'Group', 'Entry Time', 'Exit Time', 'Duration'), show='headings', height=10)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Group', text='Group')
        self.tree.heading('Entry Time', text='Entry Time')
        self.tree.heading('Exit Time', text='Exit Time')
        self.tree.heading('Duration', text='Duration')
        self.tree.pack()

    def calculate_presence(self):
        selected_name = self.id_var.get()
        selected_id = [id[0] for id in self.ids if id[1] == selected_name][0]
        start_datetime = self.start_datetime_entry.get()
        end_datetime = self.end_datetime_entry.get()

        self.cur.execute(f"""
            WITH ordered_logs AS (
              SELECT 
                face_id, 
                datetime, 
                action,
                LAG(action) OVER (PARTITION BY face_id ORDER BY datetime) as prev_action,
                LEAD(action) OVER (PARTITION BY face_id ORDER BY datetime)
                                next_action
              FROM log
              WHERE face_id = %s
                AND datetime BETWEEN %s AND %s
            ),
            filtered_logs AS (
              SELECT * FROM ordered_logs WHERE (action = 'i' AND next_action = 'o') OR (action = 'o' AND prev_action = 'i')
            ),
            grouped_logs AS (
              SELECT 
                face_id, 
                datetime, 
                action,
                SUM(CASE WHEN action = 'i' THEN 1 ELSE 0 END) OVER (PARTITION BY face_id ORDER BY datetime) as group_id
              FROM filtered_logs
            )
            SELECT 
              face_id, 
              group_id, 
              MIN(datetime) as enter_time, 
              MAX(datetime) as exit_time,
              AGE(MAX(datetime), MIN(datetime)) as duration
            FROM grouped_logs
            GROUP BY face_id, group_id
            ORDER BY enter_time;
            """, (selected_id, start_datetime, end_datetime))

        presence_entries = self.cur.fetchall()

        # Clear table
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Add data to the table
        for entry in presence_entries:
            self.tree.insert('', 'end', values=entry)








class CameraSelectKisiEkle:
    def __init__(self, master):
        self.master = master
        self.master.title("Kamera Seçimi")
        self.master.configure(background='#F5F5F5')

        self.BagliCams = get_camera_list()
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
        print(self.camera_list.get())
        camera_number_str = self.camera_list.get().split("Kamera ")[1]
        print(camera_number_str)
        CameraWindowKisiEkle.recognation(self, camera_number_str)


class CameraWindowKisiEkle:
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

    def recognation(self, cam_No):
        db_file = os.path.join(sys.path[0], 'encodeToDBWithCam.py')
        subprocess.Popen(['python', db_file, cam_No])


def open_CameraSelectKisiEkle():
    global camSelectKisiEkle
    camSelectKisiEkle = CameraSelectKisiEkle(tk.Toplevel())




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




class ShowTableWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Yoklama Tablosu")
        #self.style = ttk.Style() bu iki satır başka pencerelerin de temasını değiştiriyor
        #self.style.theme_use("clam")  # Görsel tema

        # PostgreSQL veritabanına bağlanma işlemi
        conn = DBconn()
        print(conn)

        # Tablo verilerini çeken sorgu
        cur = conn.cursor()
        cur.execute(f"SELECT id, name, status, last_reco FROM faces;")

        # Tablo verilerini bir DataFrame'e aktarma işlemi
        rows = cur.fetchall()
        self.df = pd.DataFrame(rows, columns=["ID", "İsim", "Durum", "Son Tanıma Tarihi"])
        self.df["Durum"] = self.df["Durum"].apply(lambda x: "İçeride" if x == "i" else "Dışarıda")

        # Bağlantıyı kapatma işlemi
        cur.close()
        conn.close()

        # Treeview widget'ını oluşturma işlemi
        self.tree = ttk.Treeview(self.master, show='headings')
        self.tree["columns"]=("ID", "İsim", "Durum", "Son Tanıma Tarihi")

        # Her bir sütun için başlık ve genişlik belirleme
        for column in self.tree["columns"]:
            self.tree.column(column, width=100)
            self.tree.heading(column, text=column)

        # DataFrame'deki verileri Treeview widget'ına ekleme
        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))

        # Kaydırma çubuğunu oluşturma
        self.scrollbar = ttk.Scrollbar(self.master, orient='vertical', command=self.tree.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.pack()

        # Excel Oluştur butonu
        self.save_button = ttk.Button(self.master, text="Yoklamayı Excel Dosyası Olarak Dışa Aktar", command=self.save_to_excel)
        self.save_button.pack()

    def save_to_excel(self):
        # DataFrame'i Excel dosyasına kaydetme işlemi
        save_file_path = filedialog.askdirectory()
        if save_file_path:
            datetime_str = datetime.now().strftime("%Y-%m-%d %H-%M-%S") + " Yoklaması"
            self.df.to_excel(save_file_path + f"/{datetime_str}.xlsx", sheet_name="Yoklama", index=False)




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

    start_button = tk.Button(root, text="Giriş/Çıkış Tespitni Başlat", command=open_CameraSelect,
                             width=20, height=2, bg="blue", fg="white", font=("Helvetica", 16))
    start_button.pack(padx=10, pady=10)

    add_button1 = tk.Button(root, text="Yoklama", command=lambda: ShowTableWindow(tk.Toplevel()),
                            width=20, height=2, bg="green", fg="white", font=("Helvetica", 16))
    add_button1.pack(padx=10, pady=10)

    add_button2 = tk.Button(root, text="Toplu Kişi Ekle", command=batch_add_faces,
                            width=20, height=2, bg="red", fg="white", font=("Helvetica", 16))
    add_button2.pack(padx=10, pady=10)

    start_button = tk.Button(root, text="Kamera İle Kişi Ekle", command=open_CameraSelectKisiEkle,
                             width=20, height=2, bg="blue", fg="white", font=("Helvetica", 16))
    start_button.pack(padx=10, pady=10)

    add_button1 = tk.Button(root, text="İçeride Geçirilen Zaman", command=lambda: PresenceCalculatorWindow(tk.Toplevel()),
                            width=20, height=2, bg="green", fg="white", font=("Helvetica", 16))
    add_button1.pack(padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
