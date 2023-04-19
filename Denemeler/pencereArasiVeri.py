import tkinter as tk

# örnek veri listesi
kisiler = ["Ahmet", "Mehmet", "Ayşe", "Fatma"]

def kamera_baslat():
    # Kamera başlatma kodu buraya gelebilir
    pass

def yeni_kayit_ekle():
    # Yeni kişi eklemek için
    yeni_kisi = "Yeni Kişi"
    kisiler.append(yeni_kisi)
    print("Yeni kişi eklendi:", yeni_kisi)

def liste_guncelle():
    # Listeyi güncelleyen fonksiyon
    yeni_pencere = tk.Toplevel(root)
    yeni_pencere.title("Kişi Listesi")
    yeni_pencere.geometry("200x200")
    for kisi in kisiler:
        tk.Label(yeni_pencere, text=kisi).pack()

root = tk.Tk()
root.title("Ana Menü")

# Ana menü butonları
btn_kamera_baslat = tk.Button(root, text="Kamera Başlat", command=kamera_baslat)
btn_kamera_baslat.pack()

btn_yeni_kayit_ekle = tk.Button(root, text="Yeni Kayıt Ekle", command=lambda: [yeni_kayit_ekle(), liste_guncelle()])
btn_yeni_kayit_ekle.pack()

root.mainloop()
