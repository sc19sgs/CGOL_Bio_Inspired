import tkinter as tk
from tkinter import messagebox
import subprocess

# Define a variable to hold the scheduled update_grid() task
update_task = None
root = None  # Define root variable globally

def run_script(mode):
    global update_task  # Declare update_task as global to modify it inside the function
    if update_task is not None:
        root.after_cancel(update_task)  # Cancel the scheduled update_grid() task
    if mode == "Basic CGOL":
        subprocess.Popen(["python", "CGOL2.py"])
    elif mode == "CGOL with energy bars":
        subprocess.Popen(["python", "CGOL6.py"])
    elif mode == "CGOL with infection rules":
        subprocess.Popen(["python", "CGOL_INFECTION.py"])
    elif mode == "CGOL Undless":
        subprocess.Popen(["python", "CGOL_INFECTION_UNDLESS.py"])
    else:
        messagebox.showerror("Error", "Invalid mode selected")

def main():
    global update_task, root  # Declare global variables
    root = tk.Tk()
    root.title("Mode Selector")
    
    root.geometry("400x200")

    label = tk.Label(root, text="Select Mode:")
    label.pack()

    mode_options = ["Basic CGOL", "CGOL with energy bars", "CGOL with infection rules", "CGOL Undless"]
    selected_mode = tk.StringVar(root)
    selected_mode.set(mode_options[0])

    mode_menu = tk.OptionMenu(root, selected_mode, *mode_options)
    mode_menu.pack()

    run_button = tk.Button(root, text="Run Script", command=lambda: run_script(selected_mode.get()))
    run_button.pack()

    # Add a protocol to handle closing the window
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

# Function to handle closing the Tkinter window
def on_closing():
    global update_task, root  # Declare global variables
    if update_task is not None:
        root.after_cancel(update_task)  # Cancel the scheduled update_grid() task
    root.destroy()

if __name__ == "__main__":
    main()
