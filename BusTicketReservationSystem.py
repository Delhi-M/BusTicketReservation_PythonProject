import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database setup
def setup_db():
    conn = sqlite3.connect("reservation.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
                        id INTEGER PRIMARY KEY,
                        name TEXT,      
                        age INTEGER,
                        gender TEXT,
                        seat_no INTEGER UNIQUE)''')
    conn.commit()
    conn.close()

# Book Ticket
def book_ticket():
    name = entry_name.get()
    age = entry_age.get()
    gender = gender_var.get()
    seat_no = entry_seat.get()
    
    if not (name and age and gender and seat_no):
        messagebox.showerror("Error", "All fields are required!")
        return
    
    try:
        conn = sqlite3.connect("reservation.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tickets (name, age, gender, seat_no) VALUES (?, ?, ?, ?)",
                       (name, age, gender, seat_no))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Ticket Booked Successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Seat already booked!")
    clear_entries()

# Cancel Ticket
def cancel_ticket():
    seat_no = entry_seat.get()
    if not seat_no:
        messagebox.showerror("Error", "Enter Seat Number to Cancel")
        return
    
    conn = sqlite3.connect("reservation.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tickets WHERE seat_no = ?", (seat_no,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Ticket Canceled Successfully!")
    clear_entries()

# View Booked Tickets
def view_tickets():
    conn = sqlite3.connect("reservation.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    records = cursor.fetchall()
    conn.close()
    
    ticket_window = tk.Toplevel()
    ticket_window.title("Booked Tickets")
    
    tk.Label(ticket_window, text="ID   Name   Age   Gender   Seat No").pack()
    for record in records:
        tk.Label(ticket_window, text=str(record)).pack()

# Clear Input Fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_seat.delete(0, tk.END)


# GUI Setup
root = tk.Tk()
root.title("Bus Ticket Reservation")

tk.Label(root, text="Name:").grid(row=0, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)

tk.Label(root, text="Age:").grid(row=1, column=0)
entry_age = tk.Entry(root)
entry_age.grid(row=1, column=1)

tk.Label(root, text="Gender:").grid(row=2, column=0)
gender_var = tk.StringVar(value="")
tk.Radiobutton(root, text="Male", variable=gender_var, value="Male").grid(row=2, column=1)
tk.Radiobutton(root, text="Female", variable=gender_var, value="Female").grid(row=2, column=2)

tk.Label(root, text="Seat No:").grid(row=3, column=0)
entry_seat = tk.Entry(root)
entry_seat.grid(row=3, column=1)

tk.Button(root, text="Book Ticket", command=book_ticket).grid(row=4, column=0)
tk.Button(root, text="Cancel Ticket", command=cancel_ticket).grid(row=4, column=1)
tk.Button(root, text="View Tickets", command=view_tickets).grid(row=4, column=2)

setup_db()
root.mainloop()