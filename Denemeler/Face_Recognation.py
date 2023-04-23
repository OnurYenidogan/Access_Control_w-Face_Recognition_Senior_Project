import cv2
import face_recognition

# Load the known faces and their encodings
known_face_encodings = [
    # Encoding for face 1
    [0.1, 0.2, ..., 0.9],
    # Encoding for face 2
    [0.3, 0.4, ..., 0.8],
    # ...
]

# List of names corresponding to the known face encodings
known_face_names = [
    "John",
    "Jane",
    # ...
]

# Initialize the webcam
video_capture = cv2.VideoCapture(0)

# Loop over frames from the webcam
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the frame from BGR (OpenCV's default color format) to RGB
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop over each face in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for any known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        # If a match was found, display the name of the face
        name = "Unknown"
        if True in matches:
            index = matches.index(True)
            name = known_face_names[index]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
video_capture.release()
cv2.destroyAllWindows()
