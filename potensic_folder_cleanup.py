import os
import shutil
import time
from datetime import datetime

def get_target_folder():
    """Detects current folder and asks if it should be used."""
    current_folder = os.getcwd()
    print(f"Detected working folder: {current_folder}")
    use_current = input("Is this the target folder? (yes/no): ").strip().lower()

    if use_current == 'yes':
        return current_folder
    else:
        return input("Enter the folder to organize: ").strip()

def get_file_date(file_path):
    """Extracts the date from file creation/modification time."""
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp).strftime("%Y%m%d")

def preview_changes(moves, delete_thm, delete_lrv):
    """Shows a preview of what will happen before execution."""
    print("\n--- PREVIEW OF ORGANIZATION ---")
    for dest, files in moves.items():
        print(f"\nFolder: {dest}")
        for f in files:
            print(f"  - {f}")

    if delete_thm:
        print("\n.THMs will be deleted.")
    else:
        print("\n.THMs will be kept and moved.")

    if delete_lrv:
        print("\n.LRVs will be deleted.")
    else:
        print("\n.LRVs will be kept and moved.")

    proceed = input("\nDo you want to continue with these changes? (yes/no): ").strip().lower()
    return proceed == 'yes'

def move_file_safe(src, dest):
    """Attempts to move a file safely, retrying if needed."""
    try:
        shutil.move(src, dest)
    except PermissionError:
        print(f"Warning: {src} is in use. Retrying in 5 seconds...")
        time.sleep(5)
        try:
            shutil.move(src, dest)
        except Exception as e:
            print(f"Error: Could not move {src}. Reason: {e}")

def undo_changes(changes_log):
    """Restores the original state if the user wants to undo."""
    print("\nReverting changes...")
    for original, moved in changes_log:
        move_file_safe(moved, original)
    print("Undo complete! Everything is back to the way it was.")

# Get target folder
target_folder = get_target_folder()
if not os.path.exists(target_folder):
    print("Error: The specified folder does not exist.")
    exit()

# Ask user whether to delete .THM and .LRV files
delete_thm = input("Do you want to delete .THM files? (yes/no): ").strip().lower() == 'yes'
delete_lrv = input("Do you want to delete .LRV files? (yes/no): ").strip().lower() == 'yes'

# Prepare file movements for preview
moves = {}
changes_log = []

for file in os.listdir(target_folder):
    file_path = os.path.join(target_folder, file)
    if os.path.isfile(file_path) and file.lower().endswith((".mp4", ".thm", ".lrv")):
        date_folder = get_file_date(file_path)
        dest_folder = os.path.join(target_folder, date_folder)

        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        # Determine action
        if file.lower().endswith(".thm") and delete_thm:
            moves.setdefault("To be deleted (.THM)", []).append(file)
        elif file.lower().endswith(".lrv") and delete_lrv:
            moves.setdefault("To be deleted (.LRV)", []).append(file)
        else:
            moves.setdefault(dest_folder, []).append(file)

# Preview before confirming changes
if not preview_changes(moves, delete_thm, delete_lrv):
    print("Operation canceled.")
    exit()

# Execute file organization
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

print("\nOrganization complete! Files are sorted into their respective date folders.")

# Undo option
if input("\nWould you like to undo the changes? (yes/no): ").strip().lower() == 'yes':
    undo_changes(changes_log)
