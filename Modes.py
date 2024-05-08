import tkinter as tk
from tkinter import messagebox
import subprocess

update_task = None
root = None  

def run_script(mode):
    global update_task
    if update_task is not None:
        root.after_cancel(update_task)  
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
    global update_task, root  
    root = tk.Tk()
    root.title("Mode Selector")
    root.geometry("400x200")
    root.configure(bg="light blue")
    
    logo_top_left = tk.PhotoImage(file="mouse.png").subsample(10)
    logo_top_right = tk.PhotoImage(file="wolf.png").subsample(10)
    
    label_top_left = tk.Label(root, image=logo_top_left, bg="light blue")
    label_top_left.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
    
    label_top_right = tk.Label(root, image=logo_top_right, bg="light blue")
    label_top_right.grid(row=0, column=7, sticky="ne", padx=10, pady=10)

    label = tk.Label(root, text="Select Mode:", font=("Arial", 14), bg="light grey")
    label.grid(row=1, column=0, columnspan=2, pady=(10, 5))

    mode_options = ["Basic CGOL", "CGOL with energy bars", "CGOL with infection rules", "CGOL Undless"]
    selected_mode = tk.StringVar(root)
    selected_mode.set(mode_options[0])

    mode_menu = tk.OptionMenu(root, selected_mode, *mode_options)
    mode_menu.config(font=("Arial", 12), bg="light grey")
    mode_menu.grid(row=2, column=0, columnspan=2, pady=(0, 10))

    run_button = tk.Button(root, text="Run Script", command=lambda: run_script(selected_mode.get()), font=("Arial", 12), bg="light grey")
    run_button.grid(row=3, column=0, columnspan=2, pady=10)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

def on_closing():
    global update_task, root  
    if update_task is not None:
        root.after_cancel(update_task)  
    root.destroy()

if __name__ == "__main__":
    main()
