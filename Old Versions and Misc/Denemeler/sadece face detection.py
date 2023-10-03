import threading
import tkinter as tk
import cv2


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Ana Pencere")
        self.attributes('-fullscreen', False)
        self.resizable(True, True)

        self.label = tk.Label(self, text="Kamerayı açmak için başla düğmesine basın.")
        self.label.pack(pady=20)

        self.button_start = tk.Button(self, text="Başla", command=self.start_recognition)
        self.button_start.pack(pady=10)

        self.button_stop = tk.Button(self, text="Durdur", command=self.stop_recognition, state=tk.DISABLED)
        self.button_stop.pack(pady=10)

        self.thread = None
        self.stop_event = threading.Event()

    def start_recognition(self):
        self.thread = threading.Thread(target=self.recognition_thread, args=(self.stop_event,))
        self.thread.start()

        self.button_start.config(state=tk.DISABLED)
        self.button_stop.config(state=tk.NORMAL)

    def stop_recognition(self):
        self.stop_event.set()

        self.button_start.config(state=tk.NORMAL)
        self.button_stop.config(state=tk.DISABLED)

    def recognition_thread(self, stop_event):
        # Kamera yakalama nesnesini başlatın
        cap = cv2.VideoCapture(0)

        # Haarcascade sınıflandırıcısını yükleyin
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        while not stop_event.is_set():
            # Kameradan bir görüntü yakalayın
            ret, frame = cap.read()

            # Görüntüyü gri tonlamaya dönüştürün
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Yüzleri algılayın
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Yüzlerin etrafına dikdörtgen çizin
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Görüntüyü Tkinter penceresine yansıtın
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = tk.PhotoImage(data=cv2.imencode('.png', frame)[1].tobytes())
            self.label.config(image=image)
            self.label.image = image

        # Kamera yakalama nesnesini durdurun
        cap.release()

        # Tkinter penceresini kapatın
        self.destroy()


if __name__ == '__main__':
    window = MainWindow()
    window.mainloop()
