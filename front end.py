import tkinter as tk
from tkinter import messagebox
import psycopg2

def connect_db():
    return psycopg2.connect(
        dbname="DBMS_project",  
        user="postgres",         
        password="HamzaSaeed2314",
        host="localhost",
        port="5432"
    )

def run_query(query, params=None):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(query, params or ())
    try:
        result = cur.fetchall()
    except:
        result = []
    conn.commit()
    conn.close()
    return result

# Patient View Functions 
def view_available_dentists():
    data = run_query("SELECT * FROM get_available_dentists();")
    result = "\n".join([f"{row[0]} ({row[1]})" for row in data])
    messagebox.showinfo("Available Dentists", result or "No dentists available.")

def view_total_dentists():
    total = run_query("SELECT * FROM get_total_dentists();")[0][0]
    messagebox.showinfo("Total Dentists", f"Total Dentists: {total}")

def search_by_specialization():
    def search():
        spec = entry.get()
        data = run_query("SELECT * FROM get_dentists_by_specialization(%s);", (spec,))
        result = "\n".join([f"{row[0]} ({row[1]}) - Available: {row[2]}" for row in data])
        messagebox.showinfo("Search Results", result or "No match found.")
    
    popup = tk.Toplevel()
    popup.title("Search by Specialization")
    tk.Label(popup, text="Enter Specialization:").pack()
    entry = tk.Entry(popup)
    entry.pack()
    tk.Button(popup, text="Search", command=search).pack()

# Dentist View Functions
def view_all_patients():
    data = run_query("SELECT * FROM get_patient_details();")
    result = "\n".join([f"{row[0]}, Age: {row[1]}, Ailment: {row[2]}, Dentist: {row[3]} ({row[4]})" for row in data])
    messagebox.showinfo("All Patients", result or "No patients found.")

def view_patient_counts():
    data = run_query("SELECT * FROM get_patient_counts_per_dentist();")
    result = "\n".join([f"{row[0]}: {row[1]} patients" for row in data])
    messagebox.showinfo("Patients per Dentist", result)

def view_ailment_stats():
    data = run_query("SELECT * FROM get_ailment_stats();")
    result = "\n".join([f"{row[0]}: {row[1]}" for row in data])
    messagebox.showinfo("Ailment Stats", result)

# View Definitions 
def open_patient_view():
    window = tk.Toplevel()
    window.title("Patient View")
    tk.Button(window, text="View Available Dentists", command=view_available_dentists).pack(pady=5)
    tk.Button(window, text="View Total Dentists", command=view_total_dentists).pack(pady=5)
    tk.Button(window, text="Search by Specialization", command=search_by_specialization).pack(pady=5)

def open_dentist_view():
    window = tk.Toplevel()
    window.title("Dentist View")
    tk.Button(window, text="View All Patients", command=view_all_patients).pack(pady=5)
    tk.Button(window, text="Patient Counts per Dentist", command=view_patient_counts).pack(pady=5)
    tk.Button(window, text="Ailment Stats", command=view_ailment_stats).pack(pady=5)
    tk.Button(window, text="View Available Dentists", command=view_available_dentists).pack(pady=5)
    tk.Button(window, text="Search by Specialization", command=search_by_specialization).pack(pady=5)

# Main Window
# root = tk.Tk()
# root.title("Dental Clinic Management System")
# root.geometry("400x300")

# tk.Label(root, text="Welcome to Dental Clinic", font=("Arial", 16)).pack(pady=20)
# tk.Button(root, text="Patient View", width=20, command=open_patient_view).pack(pady=10)
# tk.Button(root, text="Dentist View", width=20, command=open_dentist_view).pack(pady=10)

root = tk.Tk()
root.title("Dental Clinic Management System")
root.geometry("400x300")
root.configure(bg="lightblue")

label = tk.Label(root, text="Welcome to Dental Clinic", font=("Arial", 16), bg="lightblue")
label.pack(pady=20)

btn1 = tk.Button(root, text="Patient View", width=20, command=open_patient_view)
btn1.pack(pady=10)

btn2 = tk.Button(root, text="Dentist View", width=20, command=open_dentist_view)
btn2.pack(pady=10)

root.mainloop()
