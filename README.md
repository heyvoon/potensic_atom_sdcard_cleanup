Sure! Here's a well-structured description you can use for your **GitHub repository**:

---

# **Potensic Drone Folder Organizer**  
### **Automated Cleanup & Organization Tool for Drone Footage**  

This project provides a **Python-based tool** for organizing Potensic drone footage. It automatically sorts `.MP4`, `.THM`, and `.LRV` files into folders based on their **creation date**, while offering options to delete unnecessary files and move the `100DRONE` folder to a different location.

## **Features**
✅ **Automatic Date-Based Organization** – Files are grouped into folders based on their **creation date** (YYYYMMDD format).  
✅ **User-Controlled Cleanup** – Users can **choose** whether to delete `.THM` and `.LRV` files before organizing.  
✅ **Undo Functionality** – Provides the ability to revert all changes in case of mistakes.  
✅ **GUI Version with Tkinter** – A **user-friendly graphical interface** allows folder selection, deletion preferences, and easy management.  
✅ **Standalone Executable Support** – Easily converts to an `.exe` for **Windows users** using `PyInstaller`.  
✅ **Safe File Handling** – Handles **locked files** by implementing smart retries to avoid permission errors.  

## **How It Works**
1. **Select the target folder** where your drone footage is stored.  
2. **Choose whether to delete `.THM` and `.LRV` files** or keep them.  
3. **Preview changes** before execution.  
4. **Run the cleanup & organization** to sort files into date-based folders.  
5. **Optionally move the `100DRONE` folder** to another drive or directory.  
6. **Undo changes** if needed.  

## **Installation & Usage**
### **For the CLI Version**
Run the script using Python:
```sh
python potensic_folder_cleanup.py
```
### **For the GUI Version**
Execute:
```sh
python potensic_gui.py
```
### **Convert to `.exe`**
To package the GUI version into an executable:
```sh
pyinstaller --onefile --windowed potensic_gui.py
```

## **Requirements**
- **Python 3.x**
- **PyInstaller** (optional, for making an executable)
- **Tkinter** (pre-installed with Python for GUI version)

This tool ensures **efficient management of drone footage**, making it easier for users to **sort, clean up, and organize files** without manual effort. 🚀  

---

Would you like me to refine this further or add additional sections, such as **screenshots or examples** for the README?  
