import os
import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from tkinter import ttk
from tkinter import simpledialog
from datetime import datetime

# Function to list all the log files
def get_log_files():
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    log_files = [f for f in os.listdir(logs_dir) if f.endswith('.log')]
    return log_files

# Function to read and display the logs from the selected log file
def display_log_file(file_name):
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    log_file_path = os.path.join(logs_dir, file_name)
    
    # Read log file using pandas
    try:
        # Read log file into a dataframe
        with open(log_file_path, 'r') as file:
            logs = file.readlines()

        # Prepare the data for the table (parse each log entry)
        log_entries = []
        for log in logs:
            try:
                log_parts = log.split(' ')
                timestamp = ' '.join(log_parts[:2])  # e.g., "2025-05-07 13:10:07,877"
                level = log_parts[2]  # e.g., "INFO"
                module_info = log_parts[3].strip('[]')  # e.g., "app:90"
                message = ' '.join(log_parts[4:])  # The actual message

                log_entries.append([timestamp, level, module_info, message])
            except Exception as e:
                print(f"Error parsing log: {e}")
        
        # Convert to DataFrame
        df = pd.DataFrame(log_entries, columns=["Timestamp", "Level", "Module", "Message"])

        # Add Serial Number dynamically
        df.insert(0, "S.No", range(1, len(df) + 1))

        # Update the table
        update_table(df)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to read the log file: {e}")

# Function to update the table with log data
def update_table(df):
    for row in treeview.get_children():
        treeview.delete(row)
    
    for i, row in df.iterrows():
        treeview.insert("", "end", values=list(row))

# Function to handle file selection via Listbox
def on_select_log_file_from_list(event=None):
    selected_file = log_listbox.get(tk.ACTIVE)  # Get the selected filename
    if selected_file:
        display_log_file(selected_file)
    else:
        messagebox.showwarning("No File Selected", "Please select a log file from the list.")

# Function to display log files in a Listbox for selection (Mouse or Keyboard)
def display_log_file_selection_window():
    log_files = get_log_files()
    if not log_files:
        messagebox.showwarning("No Logs", "No log files found in the logs directory.")
        return

    # Create a new window for file selection
    selection_window = tk.Toplevel(root)
    selection_window.title("Select Log File")
    selection_window.geometry("400x300")

    # Create a Listbox with log files
    global log_listbox
    log_listbox = tk.Listbox(selection_window, height=15, width=50)
    log_listbox.pack(padx=10, pady=10)

    # Insert available log files into the Listbox
    for file in log_files:
        log_listbox.insert(tk.END, file)

    # Bind keyboard 'Enter' key to select the file
    log_listbox.bind("<Return>", on_select_log_file_from_list)

    # Add a label to guide user to press Enter or click to select
    label = tk.Label(selection_window, text="Select a log file by clicking or pressing Enter.")
    label.pack(pady=10)

    # Create a Cancel button to close the window
    cancel_button = tk.Button(selection_window, text="Cancel", command=selection_window.destroy)
    cancel_button.pack(pady=5)

# Function to handle loading log files (button click)
def on_select_log_file():
    display_log_file_selection_window()

# Function to update the system time (used for live timer and date at the bottom)
def update_time():
    # Get the current date and time with the desired format
    current_time = datetime.now().strftime("%A, %B %d, %Y - %I:%M:%S %p")  # Example: "Monday, May 07, 2025 - 03:30:15 PM"
    
    # Update the label with the current formatted time
    time_label.config(text=f"Current Date and Time: {current_time}")
    
    # Call the update_time function every 1000 ms (1 second) to refresh the time
    root.after(1000, update_time)

# Main GUI window
root = tk.Tk()
root.title("Log File Viewer")
root.geometry("800x600")

# Create a frame to hold the Treeview and scrollbars
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a Treeview to display logs
columns = ("S.No", "Timestamp", "Level", "Module", "Message")
treeview = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")

# Configure the treeview columns
for col in columns:
    treeview.heading(col, text=col)
    treeview.column(col, anchor=tk.W, width=150)

# Create vertical scrollbar for Treeview
vsb = tk.Scrollbar(frame, orient="vertical", command=treeview.yview)
vsb.pack(side="right", fill="y")

# Link the vertical scrollbar with the treeview widget
treeview.config(yscrollcommand=vsb.set)

# Pack the Treeview widget inside the frame
treeview.pack(fill=tk.BOTH, expand=True)

# Create a button to load logs
load_button = tk.Button(root, text="Load Log Files", command=on_select_log_file)
load_button.pack(pady=20)

# Create a label at the bottom to show the current date and time with bold, formatted text
time_label = tk.Label(root, text="Current Date and Time: ", anchor="w", padx=10, pady=5,
                      font=("Helvetica", 14, "bold"), fg="blue")  # Bold and Blue font
time_label.pack(side="bottom", fill="x")

# Start the live timer and date update
update_time()

# Start the application
root.mainloop()
