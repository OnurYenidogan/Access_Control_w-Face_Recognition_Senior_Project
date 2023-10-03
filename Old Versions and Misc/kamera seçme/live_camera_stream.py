import cv2

def live_camera_stream(camera_number):
    cap = cv2.VideoCapture(camera_number, cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Live Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys
    camera_number = int(sys.argv[1])
    live_camera_stream(camera_number)
