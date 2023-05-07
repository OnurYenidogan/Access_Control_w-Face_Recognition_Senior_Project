import cv2

def get_camera_list():
    camera_list = []
    index = 0
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cap.read()[0]:
            break
        else:
            camera_name = str(index)
            camera_list.append(camera_name)
        cap.release()
        index += 1
    return camera_list

camera_list = get_camera_list()

for camera_name in camera_list:
    cap = cv2.VideoCapture(int(camera_name), cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Camera " + camera_name, frame)
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
