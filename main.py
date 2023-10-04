import tkinter as tk
from tkinter import ttk
from some_functions import get_camera_list, DBconn, DBconnCheck
import subprocess
import os
import sys
import pandas as pd
from tkinter import filedialog
import configparser
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime
from datetime import datetime, time, timedelta

from PIL import Image, ImageTk

global lang
lang = "Eng"


def set_language(lang_code):
    global lang
    lang = lang_code
    # Here, you can perform necessary actions when the language changes.
    # For example, you can update your page or change translation texts.

    # Destroy the current window and create a new one to refresh the content
    root.destroy()
    main()  # A function to create the main window again

"""Gereksiz olanlar projeden kaldırılmadığı için burada yazıyor"""

"""global pgConn
pgConn = DBconn()"""


class LogSearchWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Log Sorgulama")

        # PostgreSQL veritabanına bağlanma işlemi
        self.conn = DBconn()

        # SQL sorgusu ile faces tablosundan isimleri ve log tablosundan camera_id'leri çekme
        cur = self.conn.cursor()
        cur.execute("SELECT DISTINCT name FROM faces;")
        self.names = [name[0] for name in cur.fetchall()]
        cur.execute("SELECT DISTINCT camera_id FROM log;")
        self.camera_ids = [str(id[0]) for id in cur.fetchall()]
        cur.close()

        # Faces isimlerinin bulunduğu dropdown menü
        self.name_label = ttk.Label(master, text="Yüz İsmi:")
        self.name_label.pack()
        self.name_var = tk.StringVar()
        self.name_dropdown = ttk.Combobox(master, textvariable=self.name_var, values=["Hepsi"] + self.names)
        self.name_dropdown.current(0)
        self.name_dropdown.pack()

        # Tarih aralığı belirtme radio butonları
        self.date_range_var = tk.StringVar()
        self.date_range_var.set("no")
        self.no_date_range_radio = ttk.Radiobutton(master, text="Tarih Aralığı Belirtme", variable=self.date_range_var, value="no", command=self.toggle_date_entries)
        self.no_date_range_radio.pack()
        self.yes_date_range_radio = ttk.Radiobutton(master, text="Tarih Aralığı Belirt", variable=self.date_range_var, value="yes", command=self.toggle_date_entries)
        self.yes_date_range_radio.pack()

        # Tarih ve saat girişi için başlangıç ve bitiş alanları
        self.start_label = ttk.Label(master, text="Başlangıç (Tarih - Saat)")
        self.start_label.pack()

        self.start_frame = ttk.Frame(master)
        self.start_frame.pack()

        self.start_date_entry = DateEntry(self.start_frame, state="disabled")
        self.start_date_entry.pack(side="left")

        self.start_time_frame = ttk.Frame(self.start_frame)
        self.start_time_frame.pack(side="left", padx=4)

        self.start_hour_spin = tk.Spinbox(self.start_time_frame, from_=0, to=23, width=2, format="%02.0f", state="disabled")
        self.start_hour_spin.pack(side="left")
        self.start_minute_spin = tk.Spinbox(self.start_time_frame, from_=0, to=59, width=2, format="%02.0f", state="disabled")
        self.start_minute_spin.pack(side="left")
        self.start_second_spin = tk.Spinbox(self.start_time_frame, from_=0, to=59, width=2, format="%02.0f", state="disabled")
        self.start_second_spin.pack(side="left")

        self.end_label = ttk.Label(master, text="Bitiş (Tarih - Saat)")
        self.end_label.pack()

        self.end_frame = ttk.Frame(master)
        self.end_frame.pack()

        self.end_date_entry = DateEntry(self.end_frame, state="disabled")
        self.end_date_entry.pack(side="left")

        self.end_time_frame = ttk.Frame(self.end_frame)
        self.end_time_frame.pack(side="left", padx=4)

        self.end_hour_spin = tk.Spinbox(self.end_time_frame, from_=0, to=23, width=2, format="%02.0f", state="disabled")
        self.end_hour_spin.pack(side="left")
        self.end_minute_spin = tk.Spinbox(self.end_time_frame, from_=0, to=59, width=2, format="%02.0f", state="disabled")
        self.end_minute_spin.pack(side="left")
        self.end_second_spin = tk.Spinbox(self.end_time_frame, from_=0, to=59, width=2, format="%02.0f", state="disabled")
        self.end_second_spin.pack(side="left")

        # Action için dropdown menü
        self.action_label = ttk.Label(master, text="Action:")
        self.action_label.pack()
        self.action_var = tk.StringVar()
        self.action_dropdown = ttk.Combobox(master, textvariable=self.action_var, values=["Hepsi", "i", "o"])
        self.action_dropdown.current(0)
        self.action_dropdown.pack()

        # Camera ID için dropdown menü
        self.camera_id_label = ttk.Label(master, text="Kamera ID:")
        self.camera_id_label.pack()
        self.camera_id_var = tk.StringVar()
        self.camera_id_dropdown = ttk.Combobox(master, textvariable=self.camera_id_var, values=["Hepsi"] + self.camera_ids)
        self.camera_id_dropdown.current(0)
        self.camera_id_dropdown.pack()

        # Sorgulama butonu
        self.search_button = ttk.Button(master, text="Sorgula", command=self.search)
        self.search_button.pack()

        # Results area
        self.tree_frame = tk.Frame(master)
        self.tree_frame.pack(fill='both', expand=True)

        self.tree = ttk.Treeview(self.tree_frame)
        self.tree["columns"] = ("log_id", "face_id", "name", "datetime", "action", "camera_id")

        self.tree.column("#0", width=0, minwidth=0, stretch=False)
        self.tree.column("log_id", anchor="w", width=80)
        self.tree.column("face_id", anchor="w", width=80)
        self.tree.column("name", anchor="w", width=80)
        self.tree.column("datetime", anchor="w", width=120)
        self.tree.column("action", anchor="w", width=80)
        self.tree.column("camera_id", anchor="w", width=80)

        self.tree.heading("#0", text="", anchor="w")
        self.tree.heading("log_id", text="Log ID", anchor="w")
        self.tree.heading("face_id", text="Face ID", anchor="w")
        self.tree.heading("name", text="Name", anchor="w")
        self.tree.heading("datetime", text="Date/Time", anchor="w")
        self.tree.heading("action", text="Action", anchor="w")
        self.tree.heading("camera_id", text="Camera ID", anchor="w")






        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')
        self.tree.pack(side='left', fill='both', expand=True)

    def toggle_date_entries(self):
        if self.date_range_var.get() == "yes":
            self.start_date_entry.config(state="normal")
            self.start_hour_spin.config(state="normal")
            self.start_minute_spin.config(state="normal")
            self.start_second_spin.config(state="normal")
            self.end_date_entry.config(state="normal")
            self.end_hour_spin.config(state="normal")
            self.end_minute_spin.config(state="normal")
            self.end_second_spin.config(state="normal")
        else:
            self.start_date_entry.config(state="disabled")
            self.start_hour_spin.config(state="disabled")
            self.start_minute_spin.config(state="disabled")
            self.start_second_spin.config(state="disabled")
            self.end_date_entry.config(state="disabled")
            self.end_hour_spin.config(state="disabled")
            self.end_minute_spin.config(state="disabled")
            self.end_second_spin.config(state="disabled")

    def search(self):
        name = self.name_var.get() if self.name_var.get() != "Hepsi" else "%"
        date_range = self.date_range_var.get()
        action = self.action_var.get() if self.action_var.get() != "Hepsi" else "%"
        camera_id = self.camera_id_var.get() if self.camera_id_var.get() != "Hepsi" else "%"

        if date_range == "yes":
            start_date = self.start_date_entry.get_date()
            start_time = time(int(self.start_hour_spin.get()), int(self.start_minute_spin.get()),
                              int(self.start_second_spin.get()))
            start_datetime = datetime.combine(start_date, start_time).strftime('%Y-%m-%d %H:%M:%S')

            end_date = self.end_date_entry.get_date()
            end_time = time(int(self.end_hour_spin.get()), int(self.end_minute_spin.get()),
                            int(self.end_second_spin.get()))
            end_datetime = datetime.combine(end_date, end_time).strftime('%Y-%m-%d %H:%M:%S')

            query = f"SELECT log.id, log.face_id, faces.name, log.datetime, log.action, log.camera_id FROM log JOIN faces ON log.face_id = faces.id WHERE faces.name LIKE '{name}' AND log.datetime BETWEEN '{start_datetime}' AND '{end_datetime}' AND log.action LIKE '{action}' AND CAST(log.camera_id AS TEXT) LIKE '{camera_id}';"
        else:
            query = f"SELECT log.id, log.face_id, faces.name, log.datetime, log.action, log.camera_id FROM log JOIN faces ON log.face_id = faces.id WHERE faces.name LIKE '{name}' AND log.action LIKE '{action}' AND CAST(log.camera_id AS TEXT) LIKE '{camera_id}';"

        cur = self.conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()

        for i in self.tree.get_children():
            self.tree.delete(i)

        if rows:
            for row in sorted(rows, key=lambda x: x[0]):  # ID'ye göre küçükten büyüğe sıralama
                self.tree.insert("", "end", values=row)
        else:
            messagebox.showinfo("Sonuç", "Sorgu sonucunda hiç veri bulunamadı.")


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
        self.id_label = ttk.Label(master, text="Kişi Adı")
        self.id_label.pack()
        self.id_var = tk.StringVar()
        self.id_dropdown = ttk.Combobox(master, textvariable=self.id_var, values=[id[1] for id in self.ids])
        self.id_dropdown.pack(pady=4)

        self.start_label = ttk.Label(master, text="Başlangıç (Tarih - Saat)")
        self.start_label.pack()

        self.start_frame = ttk.Frame(master)
        self.start_frame.pack()

        self.start_date_entry = DateEntry(self.start_frame)
        self.start_date_entry.pack(side="left")

        self.start_time_frame = ttk.Frame(self.start_frame)
        self.start_time_frame.pack(side="left", padx=4)

        self.start_hour_spin = tk.Spinbox(self.start_time_frame, from_=0, to=23, width=2)
        self.start_hour_spin.pack(side="left")
        self.hour_label = ttk.Label(self.start_time_frame, text="h")
        self.hour_label.pack(side="left")

        self.start_minute_spin = tk.Spinbox(self.start_time_frame, from_=0, to=59, width=2)
        self.start_minute_spin.pack(side="left")
        self.minute_label = ttk.Label(self.start_time_frame, text="m")
        self.minute_label.pack(side="left")

        self.start_second_spin = tk.Spinbox(self.start_time_frame, from_=0, to=59, width=2)
        self.start_second_spin.pack(side="left")
        self.second_label = ttk.Label(self.start_time_frame, text="s")
        self.second_label.pack(side="left")

        self.end_label = ttk.Label(master, text="Bitiş (Tarih - Saat)")
        self.end_label.pack()

        self.end_frame = ttk.Frame(master)
        self.end_frame.pack()

        self.end_date_entry = DateEntry(self.end_frame)
        self.end_date_entry.pack(side="left")

        self.end_time_frame = ttk.Frame(self.end_frame)
        self.end_time_frame.pack(side="left", padx=4)

        self.end_hour_spin = tk.Spinbox(self.end_time_frame, from_=0, to=23, width=2)
        self.end_hour_spin.pack(side="left")
        self.hour_label = ttk.Label(self.end_time_frame, text="h")
        self.hour_label.pack(side="left")

        self.end_minute_spin = tk.Spinbox(self.end_time_frame, from_=0, to=59, width=2)
        self.end_minute_spin.pack(side="left")
        self.minute_label = ttk.Label(self.end_time_frame, text="m")
        self.minute_label.pack(side="left")

        self.end_second_spin = tk.Spinbox(self.end_time_frame, from_=0, to=59, width=2)
        self.end_second_spin.pack(side="left")
        self.second_label = ttk.Label(self.end_time_frame, text="s")
        self.second_label.pack(side="left")

        self.calculate_button = ttk.Button(master, text="Hesapla", command=self.calculate_presence)
        self.calculate_button.pack()

        # Toplam süre etiketi oluşturma
        self.total_presence_label = ttk.Label(master)
        self.total_presence_label.pack()

        # Tablo oluşturma
        self.tree = ttk.Treeview(master, columns=('ID', 'Entry Time', 'Exit Time', 'Duration'), show='headings',
                                 height=10)
        self.tree.heading('ID', text='Yüz ID')
        self.tree.heading('Entry Time', text='Giriş Zamanı')
        self.tree.heading('Exit Time', text='Çıkış  Zamanı')
        self.tree.heading('Duration', text='İçeride Geçirilen Zaman')
        self.tree.pack()

    def calculate_presence(self):
        selected_name = self.id_var.get()
        matching_ids = [id[0] for id in self.ids if id[1] == selected_name]

        # Check if there are any matching IDs
        if not matching_ids:
            print(f"No matching IDs found for name: {selected_name}")
            return

        selected_id = matching_ids[0]

        start_date = self.start_date_entry.get_date()
        start_time = time(int(self.start_hour_spin.get()), int(self.start_minute_spin.get()),
                          int(self.start_second_spin.get()))
        start_datetime = datetime.combine(start_date, start_time).strftime('%Y-%m-%d %H:%M:%S')

        end_date = self.end_date_entry.get_date()
        end_time = time(int(self.end_hour_spin.get()), int(self.end_minute_spin.get()),
                        int(self.end_second_spin.get()))
        end_datetime = datetime.combine(end_date, end_time).strftime('%Y-%m-%d %H:%M:%S')

        end_date = self.end_date_entry.get_date()
        end_time = time(int(self.end_hour_spin.get()), int(self.end_minute_spin.get()),
                        int(self.end_second_spin.get()))
        end_datetime = datetime.combine(end_date, end_time).strftime('%Y-%m-%d %H:%M:%S')

        self.cur.execute(f"""
            WITH ordered_logs AS (
              SELECT 
                face_id, 
                datetime, 
                action,
                LAG(action) OVER (PARTITION BY face_id ORDER BY datetime) as prev_action,
                LEAD(action) OVER (PARTITION BY face_id ORDER BY datetime) next_action
              FROM log
              WHERE face_id = %s
                AND datetime BETWEEN %s AND %s
            ),
            filtered_logs AS (
              SELECT * FROM ordered_logs WHERE (action = 'i' AND (next_action = 'o' OR next_action IS NULL)) OR (action = 'o' AND prev_action = 'i')
            ),
            grouped_logs AS (
              SELECT 
                face_id, 
                datetime, 
                action,
                SUM(CASE WHEN action = 'i' THEN 1 ELSE 0 END) OVER (PARTITION BY face_id ORDER BY datetime) as group_id
              FROM filtered_logs
            ),
            duration_logs AS (
              SELECT 
                face_id, 
                group_id, 
                MIN(datetime) as enter_time, 
                CASE 
                  WHEN MAX(action) = 'i' THEN %s 
                  ELSE MAX(datetime) 
                END as exit_time
              FROM grouped_logs
              GROUP BY face_id, group_id
            )
            SELECT 
              face_id, 
              group_id, 
              enter_time, 
              exit_time,
              AGE(exit_time, enter_time) as duration
            FROM duration_logs
            ORDER BY enter_time;
            """, (selected_id, start_datetime, end_datetime, end_datetime))

        presence_entries = self.cur.fetchall()

        # Clear table
        for i in self.tree.get_children():
            self.tree.delete(i)

        total_presence_seconds = 0  # Toplam süreyi hesaplamak için bir değişken
        for entry in presence_entries:
            # 'entry[1]' (group_id) değeri göz ardı edilir ve ekrana basılmaz
            self.tree.insert('', 'end', values=(entry[0], entry[2], entry[3], entry[4]))
            total_presence_seconds += entry[4].total_seconds()  # Toplam süreyi hesapla

        # Toplam süreyi timedelta ile gün, saat, dakika, saniye formatına dönüştürme
        total_presence = timedelta(seconds=total_presence_seconds)

        # Toplam süreyi etikete yazma
        self.total_presence_label['text'] = f'Toplam süre: {total_presence}'


class CameraSelectKisiEkle:
    def __init__(self, master):
        self.master = master
        self.master.title("Kamerayla Kişi Ekle")
        self.master.configure(background='#F5F5F5')

        self.BagliCams = get_camera_list()

        # Kamera listesi için dropdown
        camera_label = ttk.Label(self.master, text="Kamera Seçiniz:")
        camera_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.camera_list = ttk.Combobox(self.master, values=[f"Kamera {cam}" for cam in self.BagliCams],
                                        state='readonly', width=20)
        self.camera_list.current(0)
        self.camera_list.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Seçimi onaylamak için buton
        self.confirm_button = ttk.Button(self.master, text="Kamera Başlat", command=self.cameraStart)
        self.confirm_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="s")
        self.confirm_button.configure(style='AccentButton.TButton')

        # Butonu ortala
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.confirm_button.grid(sticky="nsew")

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

        # PostgreSQL veritabanına bağlanma işlemi
        self.conn = DBconn()

        print(self.conn)

        # Tarih ve saat için girdi alanları
        self.start_label = ttk.Label(master, text="Yoklama Zamanı (Tarih - Saat)")
        self.start_label.pack()

        self.start_frame = ttk.Frame(master)
        self.start_frame.pack()

        now = datetime.now()

        self.start_date_entry = DateEntry(self.start_frame, date_pattern='dd/mm/y', year=now.year, month=now.month,
                                          day=now.day)
        self.start_date_entry.pack(side="left")

        self.start_time_frame = ttk.Frame(self.start_frame)
        self.start_time_frame.pack(side="left", padx=4)

        self.start_hour_spin = tk.Spinbox(self.start_time_frame, from_=0, to=23, width=2, value=now.hour)
        self.start_hour_spin.pack(side="left")
        self.hour_label = ttk.Label(self.start_time_frame, text="h")
        self.hour_label.pack(side="left")

        self.start_minute_spin = tk.Spinbox(self.start_time_frame, from_=0, to=59, width=2, value=now.minute)
        self.start_minute_spin.pack(side="left")
        self.minute_label = ttk.Label(self.start_time_frame, text="m")
        self.minute_label.pack(side="left")

        self.start_second_spin = tk.Spinbox(self.start_time_frame, from_=0, to=59, width=2, value=now.second)
        self.start_second_spin.pack(side="left")
        self.second_label = ttk.Label(self.start_time_frame, text="s")
        self.second_label.pack(side="left")

        # Verileri görüntüleme ve kaydetme butonları
        self.show_button = ttk.Button(master, text="Verileri Görüntüle", command=self.show_data)
        self.show_button.pack()

        self.save_button = ttk.Button(master, text="Yoklamayı Excel Dosyası Olarak Dışa Aktar",
                                      command=self.save_to_excel, state=tk.DISABLED)
        self.save_button.pack()

        # Treeview widget'ını oluşturma işlemi
        self.tree = ttk.Treeview(self.master, show='headings')
        self.tree["columns"] = ("ID", "İsim", "Durum", "Son Tanıma Tarihi", "Kamera ID")

        # Her bir sütun için başlık ve genişlik belirleme
        column_widths = [50, 150, 80, 200, 80]  # Sütun genişliklerini burada ayarlayabilirsiniz

        for i, column in enumerate(self.tree["columns"]):
            self.tree.column(column, width=column_widths[i])
            self.tree.heading(column, text=column)

        # Kaydırma çubuğunu oluşturma
        self.scrollbar = ttk.Scrollbar(self.master, orient='vertical', command=self.tree.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.pack()

    def show_data(self):
        date = self.start_date_entry.get_date().strftime('%Y-%m-%d')
        time = self.start_hour_spin.get() + ":" + self.start_minute_spin.get() + ":" + self.start_second_spin.get()
        datetime_str = date + " " + time

        cur = self.conn.cursor()
        cur.execute("SELECT id, name FROM faces;")
        all_ids_names = cur.fetchall()
        rows = []

        for id, name in all_ids_names:
            cur.execute(
                f"SELECT action, datetime, camera_id FROM log WHERE face_id = {id} AND datetime <= '{datetime_str}' ORDER BY datetime DESC LIMIT 1;")
            last_record = cur.fetchone()
            if last_record is None:
                rows.append((id, name, "Veri Yok", "Veri Yok", "Veri Yok"))
            else:
                status = "İçeride" if last_record[0] == "i" else "Dışarıda"
                rows.append((id, name, status, last_record[1], last_record[2]))

        self.df = pd.DataFrame(rows, columns=["ID", "İsim", "Durum", "Son Tanıma Tarihi", "Kamera ID"])

        for i in self.tree.get_children():
            self.tree.delete(i)

        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))

        cur.close()

        # Verileri görüntüleme butonuna basıldığında, kaydetme butonunu aktive et
        self.save_button.configure(state=tk.NORMAL)

    def save_to_excel(self):
        save_file_path = filedialog.askdirectory()
        datetime_str = self.start_date_entry.get_date().strftime(
            '%Y-%m-%d') + "_" + self.start_hour_spin.get() + "." + self.start_minute_spin.get() + "." + self.start_second_spin.get()
        self.df.to_excel(save_file_path + f"/{datetime_str}.xlsx", sheet_name="Yoklama", index=False)


class CameraSelect:
    def __init__(self, master):
        self.master = master
        self.master.title("Kamera Başlat")
        self.master.configure(background='#F5F5F5')

        self.BagliCams = get_camera_list()

        self.camera_type = tk.StringVar(value="TypeA")

        # Kamera türü seçimi için label ve radio butonlar
        type_label = ttk.Label(self.master, text="Kamera Tipi Seçiniz:")
        type_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.typea_radio = ttk.Radiobutton(self.master, text="Giriş", variable=self.camera_type, value="TypeA")
        self.typea_radio.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.typeb_radio = ttk.Radiobutton(self.master, text="Çıkış", variable=self.camera_type, value="TypeB")
        self.typeb_radio.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # Kamera listesi için label ve dropdown
        camera_label = ttk.Label(self.master, text="Kamera Seçiniz:")
        camera_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.camera_list = ttk.Combobox(self.master, values=[f"Kamera {cam}" for cam in self.BagliCams],
                                        state='readonly', width=20)
        self.camera_list.current(0)
        self.camera_list.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="w")

        # Seçimi onaylamak için buton
        self.confirm_button = ttk.Button(self.master, text="Kamera Başlat", command=self.cameraStart)
        self.confirm_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="we")

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
    root.title("Multi-Camera Facial Recognition-Based Access Control System")
    # root.title("Çok Kamera ile Yüz Tanıma Tabanlı Giriş/Çıkış Sistemi")

    # Resim dosyalarını yükle
    BtnImg = ImageTk.PhotoImage(Image.open(os.path.join("ButtonImages", f"a{lang.capitalize()}.jpg")))
    BtnImg2 = ImageTk.PhotoImage(Image.open(os.path.join("ButtonImages", f"b{lang.capitalize()}.jpg")))
    BtnImg3 = ImageTk.PhotoImage(Image.open(os.path.join("ButtonImages", f"c{lang.capitalize()}.jpg")))
    BtnImg4 = ImageTk.PhotoImage(Image.open(os.path.join("ButtonImages", f"d{lang.capitalize()}.jpg")))
    BtnImg5 = ImageTk.PhotoImage(Image.open(os.path.join("ButtonImages", f"e{lang.capitalize()}.jpg")))
    BtnImg6 = ImageTk.PhotoImage(Image.open(os.path.join("ButtonImages", f"f{lang.capitalize()}.jpg")))
    BtnTr = ImageTk.PhotoImage(Image.open(os.path.join("ButtonImages", "TurkishFlag.png")))
    BtnEng = ImageTk.PhotoImage(Image.open(os.path.join("ButtonImages", "EnglishFlag.png")))

    # Resmi tkinter ile kullanılabilir hale getir ve boyutunu ayarla
    #image = image.resize((300, 100), Image.Resampling.LANCZOS)


    # Başlık etiketi oluştur ve yerleştir
    title_label = tk.Label(root, text="Multi-Camera Facial Recognition-Based Access Control System",font=("Helvetica", 16, "bold"))
    #title_label = tk.Label(root, text="Çok Kamera ile Yüz Tanıma Tabanlı Giriş/Çıkış Sistemi",font=("Helvetica", 16, "bold"))

    title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Butonları oluştur ve hizala
    start_button = tk.Button(root, image=BtnImg, command=open_CameraSelect)
    start_button.grid(row=1, column=0, padx=10, pady=10)

    add_button1 = tk.Button(root, image=BtnImg2, command=lambda: ShowTableWindow(tk.Toplevel()))
    add_button1.grid(row=1, column=1, padx=10, pady=10)

    add_button2 = tk.Button(root, image=BtnImg3, command=batch_add_faces)
    add_button2.grid(row=2, column=0, padx=10, pady=10)

    start_button = tk.Button(root, image=BtnImg4, command=open_CameraSelectKisiEkle)
    start_button.grid(row=2, column=1, padx=10, pady=10)

    add_button1 = tk.Button(root, image=BtnImg5, command=lambda: PresenceCalculatorWindow(tk.Toplevel()))
    add_button1.grid(row=3, column=0, padx=10, pady=10)

    add_button2 = tk.Button(root, image=BtnImg6, command=lambda: LogSearchWindow(tk.Toplevel()))
    add_button2.grid(row=3, column=1, padx=10, pady=10)

    # Create and place language selection buttons
    tr_button = tk.Button(root, image=BtnTr, command=lambda: set_language("tr"))
    tr_button.grid(row=4, column=0, padx=10, pady=10, sticky="se")

    eng_button = tk.Button(root, image=BtnEng, command=lambda: set_language("eng"))
    eng_button.grid(row=4, column=1, padx=10, pady=10, sticky="sw")

    root.mainloop()


if __name__ == "__main__":
    main()
