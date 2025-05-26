import os
import shutil
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

def get_file_date(file_path):
    """Extracts the date from file creation/modification time."""
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp).strftime("%Y%m%d")

def move_file_safe(src, dest):
    """Attempts to move a file safely, retrying if needed."""
    try:
        shutil.move(src, dest)
    except PermissionError:
        time.sleep(5)
        try:
            shutil.move(src, dest)
        except Exception as e:
            print(f"Error: Could not move {src}. Reason: {e}")

def select_folder():
    """Opens a folder selection dialog."""
    folder = filedialog.askdirectory(title="Select Folder to Organize")
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder)

def select_destination_folder():
    """Opens a folder selection dialog for moving the 100DRONE folder."""
    dest_folder = filedialog.askdirectory(title="Select Destination for 100DRONE Folder")
    dest_entry.delete(0, tk.END)
    dest_entry.insert(0, dest_folder)

def preview_changes():
    """Generates a preview of what will be organized."""
    target_folder = folder_entry.get()
    if not os.path.exists(target_folder):
        messagebox.showerror("Error", "Invalid folder path!")
        return

    delete_thm = thm_var.get()
    delete_lrv = lrv_var.get()
    moves = {}

    for file in os.listdir(target_folder):
        file_path = os.path.join(target_folder, file)
        if os.path.isfile(file_path) and file.lower().endswith((".mp4", ".thm", ".lrv")):
            date_folder = get_file_date(file_path)
            dest_folder = os.path.join(target_folder, date_folder)

            if file.lower().endswith(".thm") and delete_thm:
                moves.setdefault("To be deleted (.THM)", []).append(file)
            elif file.lower().endswith(".lrv") and delete_lrv:
                moves.setdefault("To be deleted (.LRV)", []).append(file)
            else:
                moves.setdefault(dest_folder, []).append(file)

    # Check for 100DRONE folder
    drone_folder = os.path.join(target_folder, "100DRONE")
    if os.path.exists(drone_folder):
        moves.setdefault("Move 100DRONE folder", []).append(drone_folder)

    # Update preview text
    preview_text.delete("1.0", tk.END)
    preview_text.insert(tk.END, "--- PREVIEW OF ORGANIZATION ---\n")
    for dest, files in moves.items():
        preview_text.insert(tk.END, f"\n{dest}:\n")
        for f in files:
            preview_text.insert(tk.END, f"  - {f}\n")

def execute_changes():
    """Executes the file organization based on user preferences."""
    target_folder = folder_entry.get()
    dest_folder = dest_entry.get()  # Destination for 100DRONE
    if not os.path.exists(target_folder):
        messagebox.showerror("Error", "Invalid folder path!")
        return

    delete_thm = thm_var.get()
    delete_lrv = lrv_var.get()
    changes_log = []

    for file in os.listdir(target_folder):
        file_path = os.path.join(target_folder, file)
        if os.path.isfile(file_path) and file.lower().endswith((".mp4", ".thm", ".lrv")):
            date_folder = get_file_date(file_path)
            dest_folder = os.path.join(target_folder, date_folder)

            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)

            if file.lower().endswith(".thm") and delete_thm:
                os.remove(file_path)
            elif file.lower().endswith(".lrv") and delete_lrv:
                os.remove(file_path)
            else:
                new_path = os.path.join(dest_folder, file)
                move_file_safe(file_path, new_path)
                changes_log.append((file_path, new_path))

    # Move the 100DRONE folder if user selected a destination
    drone_folder = os.path.join(target_folder, "100DRONE")
    if os.path.exists(drone_folder) and dest_folder:
        new_drone_path = os.path.join(dest_folder, "100DRONE")
        move_file_safe(drone_folder, new_drone_path)
        changes_log.append((drone_folder, new_drone_path))

    messagebox.showinfo("Success", "Organization complete!")

    global undo_log
    undo_log = changes_log

def undo_changes():
    """Restores files to their original state."""
    if not undo_log:
        messagebox.showerror("Error", "No previous changes to undo!")
        return

    for original, moved in undo_log:
        move_file_safe(moved, original)

    messagebox.showinfo("Undo", "Undo complete! Everything has been reverted.")

# Create main window
root = tk.Tk()
root.title("Potensic Folder Organizer")
root.geometry("600x550")

# Folder selection
tk.Label(root, text="Select Target Folder:").pack(pady=5)
folder_entry = tk.Entry(root, width=50)
folder_entry.pack(pady=5)
tk.Button(root, text="Browse", command=select_folder).pack(pady=5)

# Destination folder selection for 100DRONE
tk.Label(root, text="Select Destination for 100DRONE Folder:").pack(pady=5)
dest_entry = tk.Entry(root, width=50)
dest_entry.pack(pady=5)
tk.Button(root, text="Browse", command=select_destination_folder).pack(pady=5)

# Checkboxes for file deletion
thm_var = tk.BooleanVar()
lrv_var = tk.BooleanVar()
tk.Checkbutton(root, text="Delete .THM files", variable=thm_var).pack()
tk.Checkbutton(root, text="Delete .LRV files", variable=lrv_var).pack()

# Preview Button
tk.Button(root, text="Preview Changes", command=preview_changes).pack(pady=5)

# Preview text box
preview_text = tk.Text(root, height=10, width=60)
preview_text.pack()

# Execute & Undo Buttons
tk.Button(root, text="Execute Organization", command=execute_changes).pack(pady=5)
tk.Button(root, text="Undo Changes", command=undo_changes).pack(pady=5)

# Store undo log
undo_log = []

# Run GUI
root.mainloop()
