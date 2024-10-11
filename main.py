import os
from tkinter import Tk, Label, Button, messagebox
from PIL import Image, ImageTk
import subprocess

class FaceRecognitionSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System")
        self.root.geometry('1530x843+0+0')  # Window size and position

        # Image paths
        image_paths = {
            "main": 'C:\\Users\Chaitra Kamat\\Desktop\\face_recognization_system\\college_images\\stanford.jpeg',
            "banner":'C:\\Users\\Chaitra Kamat\\Desktop\\face_recognization_system\\college_images\\stanford3.jpeg' ,
            "button": 'C:\\Users\\Chaitra Kamat\\Desktop\\face_recognization_system\\college_images\\stanford2.jpeg'
        }

        # Load and display banner images
        self.photo_images = [self.load_image(image_paths["main"], (500, 130))] * 2
        self.photo_images.append(self.load_image(image_paths["main"], (550, 130)))
        self.photo_images.append(self.load_image(image_paths["banner"], (1530, 710)))

        for i, img in enumerate(self.photo_images[:3]):
            if img:
                f_lbl = Label(self.root, image=img)
                f_lbl.place(x=i * 500, y=0, width=500, height=130)

        if self.photo_images[3]:
            f4_lbl = Label(self.root, image=self.photo_images[3])
            f4_lbl.place(x=0, y=130, width=1530, height=710)

        # Title label
        title_lb = Label(self.root, text="FACE RECOGNITION ATTENDANCE SYSTEM SOFTWARE", 
                         font=("times new roman", 20, "bold"), bg="white", fg="red")
        title_lb.place(x=0, y=130, width=1530, height=40)

        # Button definitions
        button_data = [
            {"text": "STUDENT DETAILS", "pos": (100, 200), "command": self.open_student_details},
            {"text": "FACE DETECTOR", "pos": (400, 200), "command": self.open_face_detector},
            {"text": "ATTENDANCE", "pos": (700, 200), "command": self.open_attendance},
            {"text": "Attendance Sheet", "pos": (1000, 200), "command": self.open_attendance_sheet},
            {"text": "TRAIN DATA", "pos": (100, 430), "command": self.open_train_data},
            {"text": "EXIT", "pos": (400, 430), "command": self.take_attendance_and_quit}  # Modified Exit button
        ]

        # Create buttons dynamically
        for btn_data in button_data:
            self.create_button(btn_data, image_paths["button"])

    def load_image(self, path, size):
        """Load an image from the given path and resize it to the specified size."""
        try:
            img = Image.open(path)
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None

    def create_button(self, btn_data, image_path):
        """Create a button with an image and text label."""
        btn_img = self.load_image(image_path, (150, 150))
        if btn_img:
            btn = Button(self.root, image=btn_img, cursor='hand2', command=btn_data["command"])
            btn.place(x=btn_data["pos"][0], y=btn_data["pos"][1], width=150, height=150)
            btn.image = btn_img  # Keep a reference to the image to prevent garbage collection

            btn_text = Button(self.root, text=btn_data["text"], font=("times new roman", 12), bg="white", fg="red")
            btn_text.place(x=btn_data["pos"][0], y=btn_data["pos"][1] + 150, width=150, height=40)

    # Functions to open different modules or scripts
    def open_student_details(self):
        self.run_script('C:\\Users\\Chaitra Kamat\Desktop\\face_recognization_system\\student.py')

    def open_face_detector(self):
        self.run_script('C:\\Users\\Chaitra Kamat\\Desktop\\face_recognization_system\\recognizer.py')

    def open_attendance(self):
        self.run_script('C:\\Users\\Chaitra Kamat\\Desktop\\face_recognization_system\\attendance.py')

    def open_attendance_sheet(self):
        self.run_script('C:\\Users\\Chaitra Kamat\\Desktop\\face_recognization_system\\sheet.py')

    def open_train_data(self):
        self.run_script('C:\\Users\\Chaitra Kamat\\Desktop\\face_recognization_system\\phototrain.py')

    def run_script(self, script_path, quit_after=False):
        """Run a python script if the file exists."""
        if os.path.exists(script_path):
            try:
                subprocess.Popen(['python', script_path])
                if quit_after:
                    self.root.quit()
            except Exception as e:
                print(f"Error running script {script_path}: {e}")
        else:
            print(f"Script {script_path} not found.")

    def take_attendance_and_quit(self):
        """Ask the user if they want to take attendance and then quit."""
        if messagebox.askyesno("Exit", "Do you want to exit?"):
            self.root.quit()  # Quit the main application

if __name__ == "__main__":
    root = Tk()
    obj = FaceRecognitionSystem(root)
    root.mainloop()
