import pandas as pd
from tkinter import Tk, Text, Scrollbar

class ExcelViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Viewer")
        self.root.geometry('800x600')

        # Load Excel data
        excel_file = r"E:\face_recognization_system\attendance.xlsx"  # Replace with your Excel file path
        self.data = self.load_excel(excel_file)

        # Create Text widget to display Excel data
        self.text_widget = Text(self.root, wrap="none", font=("Courier New", 12), padx=10, pady=10)
        self.text_widget.pack(fill="both", expand=True)

        # Display data in Text widget
        self.display_excel_data()

        # Add scrollbar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.config(command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def load_excel(self, file_path):
        """Load data from Excel file using pandas."""
        try:
            return pd.read_excel(file_path)
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return None

    def display_excel_data(self):
        """Display Excel data in the Text widget."""
        if self.data is not None:
            # Convert DataFrame to string and display in Text widget
            data_str = self.data.to_string(index=False)
            self.text_widget.insert("1.0", data_str)
        else:
            self.text_widget.insert("1.0", "Failed to load Excel file.")

if __name__ == "__main__":
    root = Tk()
    app = ExcelViewerApp(root)
    root.mainloop()
