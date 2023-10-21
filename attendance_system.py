import cv2
import dlib
import sqlite3

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 for the default camera, change if necessary

# Load a pre-trained face detection model
face_detector = dlib.get_frontal_face_detector()

# Load a pre-trained face recognition model
face_recognizer = dlib.face_recognition_model_v1('shape_predictor_68_face_landmarks.dat')  # Download this model

# Load known faces and corresponding names from a database or file
known_faces = []  # Store face encodings
known_names = []  # Store corresponding names

# Connect to the SQLite database (create one if it doesn't exist)
db_conn = sqlite3.connect('attendance.db')

def log_attendance(name):
    cursor = db_conn.cursor()
    cursor.execute("INSERT INTO attendance (name) VALUES (?)", (name,))
    db_conn.commit()

while True:
    # Capture a frame
    ret, frame = cap.read()

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_detector(gray)

    for face in faces:
        # Get the face encodings
        face_encoding = face_recognizer(frame, face)

        # Compare the detected face with known faces
        match = False
        for i, known_face in enumerate(known_faces):
            # Compare the face encodings
            if dlib.face_distance([known_face], face_encoding)[0] < 0.6:
                name = known_names[i]
                match = True
                break

        if match:
            cv2.putText(frame, f"Welcome, {name}", (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            log_attendance(name)
        else:
            cv2.putText(frame, "Unknown", (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)

    # Display the frame with detected faces
    cv2.imshow('Attendance System', frame)

    # Exit the loop by pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera, close the database connection, and close OpenCV windows
cap.release()
db_conn.close()
cv2.destroyAllWindows()
