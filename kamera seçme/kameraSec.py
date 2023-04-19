import tkinter as tk
import cv2
import subprocess

# VideoCapture'den mevcut kameraların isimlerini bulmak için kullanılacak bir fonksiyon
def get_camera_list():
    camera_list = []
    index = 0
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cap.read()[0]:
            break
        else:
            camera_name = f"Camera {index+1}"
            camera_list.append(camera_name)
        cap.release()
        index += 1
    return camera_list

# Tkinter penceresi oluşturma
root = tk.Tk()
root.geometry("300x150")
root.title("Kamera Seçimi")

# Dropdown menü için değişken oluşturma
selected_camera = tk.StringVar()

# Bilgisayarınıza bağlı kameraların isimlerini alın
camera_list = get_camera_list()

# Dropdown menü oluşturma
camera_menu = tk.OptionMenu(root, selected_camera, *camera_list)
camera_menu.pack(pady=10)

# Kamera seçildiğinde çağrılacak fonksiyon
def select_camera():
    # Seçilen kameranın ismini alın
    camera_name = selected_camera.get()
    # Kameranın numarasını bulun
    camera_number = camera_list.index(camera_name)
    # Kamerayı açın
    cap = cv2.VideoCapture(camera_number, cv2.CAP_DSHOW)
    # Yeni bir pencere açın ve kameradan canlı görüntüyü gösterin
    subprocess.Popen(['python', 'giris_kamerasi.py', f'{camera_number}'])
    # Kamerayı kapatın
    cap.release()
    # Seçilen kameranın ismini ve numarasını yazdırın
    print("Seçilen kamera ismi:", camera_name)
    print("Seçilen kamera numarası:", camera_number)

# "Kamera Seç" düğmesi oluşturma
select_button = tk.Button(root, text="Kamera Seç", command=select_camera)
select_button.pack(pady=10)

# Tkinter penceresini çalıştırma
root.mainloop()
