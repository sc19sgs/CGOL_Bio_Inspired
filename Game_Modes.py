import tkinter as tk
from tkinter import ttk
import subprocess
import sys
from PIL import Image, ImageTk

def run_script(script_name):
    """Run the specified Python script using the same Python interpreter as the current process."""
    try:
        # Run the Python script using the same kernel so that dependencies are met
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")

class ScriptLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conway's Game of Life Modes")
        
        # Full Screen window
        self.root.attributes('-fullscreen', True)
        
        self.tab_control = ttk.Notebook(root)
        
        # Defined scripts and appropriate images
        game_modes = [
            ("CGOL2.py", "Conway's Game of Life (Predator vs Prey)", "wolf.png"),
            ("CGOL6.py", "Conway's Game of Life (Predator vs Prey [Food Supply])", "cheese.png"),
            ("CGOL_INFECTION.py", "Conway's Game of Life (Infection)", "virus.png")
        ]
        
        # Tab for each script and image assigned
        for script, description, image_file in game_modes:
            self.create_tab(script, description, image_file)
        
        self.tab_control.pack(expand=1, fill="both")

    def create_tab(self, script_name, button_text, image_file):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text=button_text)
        
        # Load the image
        image = Image.open(image_file)
        image = image.resize((64, 64), Image.Resampling.LANCZOS)  # Use LANCZOS for resizing
        photo = ImageTk.PhotoImage(image)
        
        # Create a frame to hold the button and image
        frame = tk.Frame(tab)
        frame.pack(pady=20)
        
        # Create a label for the image
        label = tk.Label(frame, image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.pack(side=tk.LEFT, padx=10)
        
        # Create a stylized button on the tab to run the script
        button = ttk.Button(frame, text=button_text, 
                            command=lambda: run_script(script_name))
        button.pack(side=tk.RIGHT, padx=10)

# Create the main window
root = tk.Tk()
app = ScriptLauncherApp(root)

# Run the application
root.mainloop()
