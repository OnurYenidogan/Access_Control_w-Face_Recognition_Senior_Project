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

# Create VideoCapture objects for each camera
cap_list = []
for camera_name in camera_list:
    cap = cv2.VideoCapture(int(camera_name), cv2.CAP_DSHOW)
    cap_list.append(cap)

# Create windows for each camera
for camera_name in camera_list:
    cv2.namedWindow("Camera " + camera_name)

# Display the live streams from all cameras
while True:
    for i, cap in enumerate(cap_list):
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Camera " + camera_list[i], frame)

    # Exit loop when 'q' is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release resources
for cap in cap_list:
    cap.release()
cv2.destroyAllWindows()
