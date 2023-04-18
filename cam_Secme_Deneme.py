import tkinter as tk
import cv2

# VideoCapture'den mevcut kameraların numaralarını bulmak için kullanılacak bir fonksiyon
def get_camera_list():
    camera_list = []
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            camera_list.append(index)
        cap.release()
        index += 1
    return camera_list

# Tkinter penceresi oluşturma
root = tk.Tk()
root.geometry("300x150")
root.title("Kamera Seçimi")

# Dropdown menü için değişken oluşturma
selected_camera = tk.StringVar()

# Bilgisayarınıza bağlı kameraların listesini alın
camera_list = get_camera_list()

# Dropdown menü oluşturma
camera_menu = tk.OptionMenu(root, selected_camera, *camera_list)
camera_menu.pack(pady=10)

# Kamera seçildiğinde çağrılacak fonksiyon
def select_camera():
    # Seçilen kameranın numarasını alın
    camera_number = int(selected_camera.get())
    # Kamerayı açın
    cap = cv2.VideoCapture(camera_number)
    # Kamera görüntüsünü okuyun
    ret, frame = cap.read()
    # Kamerayı kapatın
    cap.release()
    # Seçilen kameranın numarasını yazdırın
    print("Seçilen kamera numarası:", camera_number)

# "Kamera Seç" düğmesi oluşturma
select_button = tk.Button(root, text="Kamera Seç", command=select_camera)
select_button.pack(pady=10)

# Tkinter penceresini çalıştırma
root.mainloop()
