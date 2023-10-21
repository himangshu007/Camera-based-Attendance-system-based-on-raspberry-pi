import cv2
import dlib
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime

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

# Create a tkinter window
root = tk.Tk()
root.title("Attendance System")

# Create a label to display the camera feed
label = Label(root)
label.pack()

# Create a listbox to display recognized names
name_listbox = tk.Listbox(root)
name_listbox.pack()

attendance_log_file = open("attendance_log.txt", "a")

is_running = False  # Flag to control the attendance system

def toggle_system():
    global is_running
    if is_running:
        stop_system()
    else:
        start_system()

def start_system():
    global is_running
    is_running = True
    toggle_button.config(text="Stop System")
    update_gui()

def stop_system():
    global is_running
    is_running = False
    toggle_button.config(text="Start System")

def log_attendance(name):
    cursor = db_conn.cursor()
    cursor.execute("INSERT INTO attendance (name) VALUES (?)", (name,))
    db_conn.commit()
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    attendance_log_file.write(f"{name} - {timestamp}\n")
    attendance_log_file.flush()

def update_gui():
    if is_running:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=img)

        label.img = img
        label.config(image=img)
        
        # Insert recognized names into the listbox (simulated for this example)
        recognized_name = "John Doe"  # Replace with actual recognized name
        name_listbox.insert(tk.END, recognized_name)
        
        log_attendance(recognized_name)  # Log attendance

    root.after(10, update_gui)

# Create a toggle button to start and stop the system
toggle_button = Button(root, text="Start System", command=toggle_system)
toggle_button.pack()

update_gui()

root.mainloop()

# Release the camera, close the database connection, and close OpenCV windows
cap.release()
db_conn.close()
attendance_log_file.close()
