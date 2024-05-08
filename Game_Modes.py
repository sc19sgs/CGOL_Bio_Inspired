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
        
        # Set a fixed window size instead of full screen
        self.root.geometry("1200x800")
        
        # Set a modern theme for ttk widgets
        style = ttk.Style()
        style.theme_use('clam')  # You can experiment with 'alt', 'default', 'classic', 'clam', etc.
        style.configure('TNotebook.Tab', font=('Helvetica', 18), padding=[30, 12], background='lightblue')
        style.configure('TButton', font=('Helvetica', 14), padding=[15, 8], relief='raised', background='#007BFF', foreground='white')  # Bright blue with larger font
        style.configure('TFrame', background='white')  # Ensure frames match tab backgrounds
        
        self.tab_control = ttk.Notebook(root)
        
        # Defined scripts and appropriate images
        game_modes = [
            ("CGOL2.py", "Conway's Game of Life (Predator vs Prey)", "wolf.png", 
             "• Predators (Wolves) vs Mice (Prey)\n" + 
             "\n"+
             "   - Place mice by left-clicking on grid normally.\n" + 
             "   - Place wolves by left-clicking on grid while holding down shift.\n" + 
             "   - Both species replicate using Conway's Game of Life rules.\n" + 
             "   - Predators take precedence by being able to 'eat' the Mice and take priority in spawning."),
            ("CGOL6.py", "Conway's Game of Life (Predator vs Prey [Food Supply])", "cheese.png", 
             "• Builds on Predator vs Prey with additional elements:\n" +
            "\n"+
             "   - Randomly placed food sources (Cheese) for the Mice.\n" + 
             "   - Mice eat cheese by being one block away, triggering a spawning pattern in the grid's corner.\n" + 
             "   - Wolves are rewarded for eating Mice by spawning wolves in the grid's corner.\n" + 
             "   - A relative population bar shows the population of each species."),
            ("CGOL_INFECTION_UNDLESS.py", "Conway's Game of Life (Infection)", "virus.png", 
             "• Enhances Predator vs Prey by adding a punishment mechanism:\n" +
            "\n"+
             "   - A virus/infection attacks when relative populations exceed 70%.\n" +
             "   - This prevents overpopulation and maintains balance.")
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
        button = ttk.Button(top_frame, text=f"Start {button_text}", 
                            command=lambda: run_script(script_name), style='TButton')
        button.pack(side=tk.RIGHT, padx=10)

# Create the main window
root = tk.Tk()
app = ScriptLauncherApp(root)

# Run the application
root.mainloop()
