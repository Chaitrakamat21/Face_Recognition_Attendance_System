import openpyxl
from tkinter import Tk, Label, Button, messagebox
from PIL import ImageTk, Image
import cv2
import time

class FaceRecognitionSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1130x580+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="FACE RECOGNITION", font=("times new roman", 20, "bold"), bg="white", fg="darkgreen")
        title_lbl.place(x=0, y=0, width=1130, height=35)

        self.student_data = {}  # Dictionary to store student data
        self.load_student_data()  # Load student data from Excel file
        self.setup_images()
        self.setup_buttons()

    def load_student_data(self):
        wb = openpyxl.load_workbook("E:\\face_recognization_system\\student_data.xlsx")
        sheet = wb.active
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Assuming your data starts from row 2 (after the header)
            id = row[0]
            name = row[1]
            self.student_data[id] = name  # Store the ID and name in the dictionary
            print(f"ID: {id}, Name: {name}")  # Display the loaded data

    def setup_images(self):
        # Load and display left side image
        self.img_left_path = "college_images/stanford.jpeg"
        self.display_image(self.img_left_path, x=0, y=35, width=545, height=545)

        # Load and display right side image
        self.img_right_path = "college_images/stanford.jpeg"
        self.display_image(self.img_right_path, x=585, y=35, width=545, height=545)

    def display_image(self, img_path, x, y, width, height):
        img = Image.open(img_path)
        img = img.resize((width, height), Image.LANCZOS)
        photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root, image=photoimg)
        f_lbl.image = photoimg
        f_lbl.place(x=x, y=y, width=width, height=height)

    def setup_buttons(self):
        Button(self.root, text="START FACE RECOGNITION", command=self.face_recog, cursor="hand2", font=("times new roman", 14, "bold"), bg="green", fg="white").place(x=415, y=500, width=300, height=50)

    def get_name_from_id(self, id):
        # Use the stored student data to get the name by ID
        name = self.student_data.get(id, "unknown")
        return id, name

    def display_data_from_excel(self, id):
        name = self.student_data.get(id, "unknown")
        messagebox.showinfo("Student Data", f"ID: {id}\nName: {name}")

    def draw_boundary(self, img, classifier, scaleFactor, minNeighbors, color, clf, id_confidence_dict):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
            id, confidence = clf.predict(gray_image[y:y + h, x:x + w])
            name = self.get_name_from_id(id)[1]
            cv2.putText(img, f"ID: {id} - {name} Confidence: {confidence:.2f}%", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            if id not in id_confidence_dict or confidence > id_confidence_dict[id]:
                id_confidence_dict[id] = confidence

    def face_recog(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")
        cap = cv2.VideoCapture(0)

        start_time = time.time()
        id_confidence_dict = {}

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            self.draw_boundary(frame, face_cascade, 1.1, 10, (0, 255, 0), clf, id_confidence_dict)

            cv2.imshow('Face Recognition', frame)

            if cv2.waitKey(1) == 13 or (time.time() - start_time) > 20:
                break

        cap.release()
        cv2.destroyAllWindows()

        highest_confidence_id = max(id_confidence_dict, key=id_confidence_dict.get)
        highest_confidence = id_confidence_dict[highest_confidence_id]

        user_response = messagebox.askyesno("Confirm", f"ID: {highest_confidence_id} has the highest confidence at {highest_confidence:.2f}%. Do you want to display the data?")
        if user_response:
            self.display_data_from_excel(highest_confidence_id)

if __name__ == "__main__":
    root = Tk()
    obj = FaceRecognitionSystem(root)
    root.mainloop()
