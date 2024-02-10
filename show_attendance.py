import pandas as pd
from glob import glob
import os
import tkinter as tk
import csv

def subjectchoose(text_to_speech):
    def create_default_csv(subject_path, subject_name):
        # Create a default CSV file with expected columns
        default_data = {
            'Name': [],  # Add expected columns as needed
            'ID': [],
            'Attendance': []
        }
        default_df = pd.DataFrame(default_data)
        default_csv_path = os.path.join(subject_path, f"{subject_name}_default.csv")
        default_df.to_csv(default_csv_path, index=False)
        return default_csv_path

    def calculate_attendance():
        Subject = tx.get().strip()  # Get the subject name and strip whitespace
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return
        
        # Define the path for the subject folder
        subject_path = f"Attendance\\{Subject}"

        # Create the directory if it does not exist
        if not os.path.exists(subject_path):
            os.makedirs(subject_path)

        # Look for CSV files in the subject directory
        filenames = glob(f"{subject_path}\\{Subject}*.csv")
        if not filenames:
            # Create a default CSV if none exist
            default_csv_path = create_default_csv(subject_path, Subject)
            t = f"No attendance files found for subject '{Subject}'. A default file has been created at {default_csv_path}."
            text_to_speech(t)
            return  # Exit after informing the user

        # Read and merge the attendance CSV files
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = 0
        
        # Calculate attendance percentage
        for i in range(len(newdf)):
            newdf["Attendance"].iloc[i] = str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + '%'

        # Save the combined attendance data to a new CSV file
        newdf.to_csv(f"{subject_path}\\attendance.csv", index=False)

        # Display attendance in a new Tkinter window
        root = tk.Tk()
        root.title("Attendance of " + Subject)
        root.configure(background="black")
        
        cs = f"{subject_path}\\attendance.csv"
        with open(cs) as file:
            reader = csv.reader(file)
            r = 0

            for col in reader:
                c = 0
                for row in col:
                    label = tk.Label(
                        root,
                        width=10,
                        height=1,
                        fg="yellow",
                        font=("times", 15, " bold "),
                        bg="black",
                        text=row,
                        relief=tk.RIDGE,
                    )
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        root.mainloop()

    subject = tk.Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    # Title label
    titl = tk.Label(subject, bg="black", relief=tk.RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=tk.X)

    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    # Label and Entry for subject name
    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=tk.RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=tk.RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    # Button to view attendance
    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=tk.RIDGE,
    )
    fill_a.place(x=195, y=170)

    subject.mainloop()

# Example usage of text_to_speech function for demonstration purposes
def text_to_speech(message):
    print(message)  # Replace this with actual TTS functionality if needed

# Run the application
subjectchoose(text_to_speech)
