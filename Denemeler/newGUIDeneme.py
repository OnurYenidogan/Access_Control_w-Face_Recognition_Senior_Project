from PIL import Image, ImageTk
import tkinter as tk

def on_button_click(event):
    print("Butona tıklandı!")

root = tk.Tk()

# Resim dosyasını yükle
image = Image.open("a.jpg")

# Resmi tkinter ile kullanılabilir hale getir
photo = ImageTk.PhotoImage(image)

# Canvas oluştur
canvas = tk.Canvas(root, width=200, height=100)
canvas.pack()

# Canvas üzerine resim ekleyin
canvas.create_image(20, 20, anchor="nw", image=photo)

# Canvas üzerine başlık ve açıklama ekleyin
canvas.create_text(80, 30, text="Başlık", font=("Helvetica", 16))
canvas.create_text(80, 60, text="Açıklama", font=("Helvetica", 12))

# Canvas üzerine tıklanabilir bir dikdörtgen ekleyin
button = canvas.create_rectangle(0, 0, 200, 100, fill="", outline="")

# Dikdörtgene tıklama olayı ekleyin
canvas.tag_bind(button, "<Button-1>", on_button_click)

root.mainloop()
