import cv2
import dlib
import sqlite3
from tkinter import Tk
import face_recognition
from gui import create_gui  # Integrate GUI
from image_preprocessing import preprocess_image  # Integrate image preprocessing
from data_management import filter_attendance_data  # Integrate data management
from email_notification import send_email  # Integrate email notifications
from data_visualization import create_attendance_chart  # Integrate data visualization
from face_database_management import add_known_face, update_known_face, remove_known_face  # Integrate face database management

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 for the default camera, change if necessary

# Load a pre-trained face detection model
face_detector = dlib.get_frontal_face_detector()

# Load a pre-trained face recognition model
face_recognizer = dlib.face_recognition_model_v1('shape_predictor_68_face_landmarks.dat')  # Download this model

# Connect to the SQLite database for known faces
known_faces_db_conn = sqlite3.connect('known_faces.db')
known_faces_db_cursor = known_faces_db_conn.cursor()

# Create a table to store known faces if it doesn't exist
known_faces_db_cursor.execute('''CREATE TABLE IF NOT EXISTS known_faces (
                    name TEXT PRIMARY KEY,
                    encoding BLOB)''')

# Connect to the SQLite database for attendance records
attendance_db_conn = sqlite3.connect('attendance.db')

# Create an attendance table if it doesn't exist
attendance_db_cursor = attendance_db_conn.cursor()
attendance_db_cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    name TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

# Function to recognize a face in the frame
def recognize_face(frame, face):
    # Convert the BGR frame to RGB (as required by face_recognition)
    rgb_frame = frame[:, :, ::-1]

    # Compute the face encodings for all detected faces in the frame
    face_encodings = face_recognition.face_encodings(rgb_frame, [face])

    if not face_encodings:
        return None  # No face found

    # Compare the detected face encoding to known face encodings in the database
    known_faces_db_cursor.execute("SELECT name, encoding FROM known_faces")
    for row in known_faces_db_cursor.fetchall():
        known_name, known_encoding = row[0], bytes.fromhex(row[1])
        face_distance = face_recognition.face_distance([known_encoding], face_encodings[0])

        # You can adjust the distance threshold as needed
        if face_distance[0] < 0.6:
            return known_name  # Return the recognized name

    return None  # Face not recognized

def log_attendance(name):
    # Log attendance in your attendance database
    attendance_db_cursor.execute("INSERT INTO attendance (name) VALUES (?)", (name,))
    attendance_db_conn.commit()

# Create a GUI for starting and stopping the system
root = Tk()
app = create_gui(root, cap)

while app.is_running():
    ret, frame = cap.read()

    if not app.is_system_active():
        cv2.imshow('Attendance System', frame)
        continue

    # Preprocess the frame (if needed)
    preprocessed_frame = preprocess_image(frame, width=640, height=480)

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(preprocessed_frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_detector(gray)

    for face in faces:
        recognized_name = recognize_face(preprocessed_frame, face)

        if recognized_name:
            cv2.putText(preprocessed_frame, f"Welcome, {recognized_name}", (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            log_attendance(recognized_name)
        else:
            cv2.putText(preprocessed_frame, "Unknown", (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Draw a rectangle around the detected face
        cv2.rectangle(preprocessed_frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)

    # Display the frame with detected faces
    cv2.imshow('Attendance System', preprocessed_frame)

    # Exit the loop by pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera, close the database connections, and close OpenCV windows
cap.release()
known_faces_db_conn.close()
attendance_db_conn.close()
cv2.destroyAllWindows()

