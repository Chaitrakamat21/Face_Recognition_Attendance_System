import cv2
import openpyxl
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox

class FaceRecognition:
    def __init__(self, model_path, excel_path):
        # Load the trained model
        self.clf = cv2.face.LBPHFaceRecognizer_create()
        self.clf.read(model_path)

        # Load student data from Excel
        self.excel_file = excel_path
        self.student_data = self.load_student_data(self.excel_file)

        # Load the face cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def load_student_data(self, excel_path):
        # Load student data from the provided Excel file
        wb = openpyxl.load_workbook(excel_path)
        sheet = wb.active
        student_data = {}
        for row in sheet.iter_rows(min_row=2, values_only=True):
            student_id = int(row[0])  # Ensure ID is read as an integer
            student_name = row[1]
            student_data[student_id] = student_name
        return student_data

    def recognize_faces(self):
        # Initialize webcam feed
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))
            
            for (x, y, w, h) in faces:
                # Predict the ID of the face and its confidence
                face_id, confidence = self.clf.predict(gray[y:y+h, x:x+w])
                name = self.student_data.get(face_id, "Unknown")

                # Draw rectangle around the face and label it
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, f"ID: {face_id}, Name: {name}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

            # Display the frame
            cv2.imshow('Face Recognition', frame)
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the capture and destroy all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

def start_recognition():
    try:
        model_path = "trainer.yml"
        excel_path = r"C:\Users\Chaitra Kamat\Desktop\face_recognization_system\student_data.xlsx"
        fr = FaceRecognition(model_path, excel_path)
        fr.recognize_faces()
    except FileNotFoundError as e:
        messagebox.showerror("File Not Found", str(e))
    except cv2.error as e:
        messagebox.showerror("OpenCV Error", f"OpenCV error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Set up Tkinter
    root = tk.Tk()
    root.title("Face Recognition System")

    # Create a start button
    start_button = tk.Button(root, text="Start Face Recognition", command=start_recognition)
    start_button.pack(pady=20)

    # Run the Tkinter main loop
    root.mainloop()
