import cv2


def get_camera_list():
    camera_list = []
    index = 0
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cap.read()[0]:
            break
        else:
            camera_name = index
            camera_list.append(camera_name)
        cap.release()
        index += 1
    return camera_list
