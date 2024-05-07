import tkinter as tk
from tkinter import messagebox
import subprocess

def run_script(mode):
    if mode == "Basic CGOL":
        subprocess.call(["python", "CGOL.py"])
    elif mode == "CGOL with energy bars":
        subprocess.call(["python", "CGOL3.py"])
    elif mode == "CGOL with enhanced rules":
        subprocess.call(["python", "CGOL6.py"])
    else:
        messagebox.showerror("Error", "Invalid mode selected")

def main():
    root = tk.Tk()
    root.title("Mode Selector")
    
    root.geometry("400x200")

    label = tk.Label(root, text="Select Mode:")
    label.pack()

    mode_options = ["Basic CGOL", "CGOL with energy bars", "CGOL with enhanced rules"]
    selected_mode = tk.StringVar(root)
    selected_mode.set(mode_options[0])

    mode_menu = tk.OptionMenu(root, selected_mode, *mode_options)
    mode_menu.pack()

    run_button = tk.Button(root, text="Run Script", command=lambda: run_script(selected_mode.get()))
    run_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
