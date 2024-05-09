"""
RUN THIS AS THE MAIN APPLICATION FILE:
This will provide you with Game Mode tabs and appropriate rules for each game:

- Basic CGOL Predator vs Prey 
- Food Supply Introduced
- Infection Mode Introduced
- Endless Mode

"""

import tkinter as tk
from tkinter import ttk
import subprocess
import sys
from PIL import Image, ImageTk

# Global variable to keep track of any background task or subprocess
update_task = None

def run_script(script_name):
    """Run the specified Python script using the same Python interpreter as the current process."""
    try:
        # Run the Python script using subprocess.Popen to not wait for completion
        subprocess.Popen([sys.executable, script_name])
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")

def on_closing():
    """Handle the closing of the main window and any subprocesses."""
    global update_task, root
    if update_task is not None:
        # If there's a running subprocess, terminate it
        update_task.terminate()
        update_task = None
    # Destroy the main window
    root.destroy()

class ScriptLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conway's Game of Life Modes")
        
        # Set a fixed window size instead of full screen
        self.root.geometry("1200x800")
        
        # Set a modern theme for ttk widgets
        style = ttk.Style()
        style.theme_use('clam')  # You can experiment with 'alt', 'default', 'classic', 'clam', etc.
        style.configure('TNotebook.Tab', font=('Helvetica', 10), padding=[30, 12], background='lightblue')
        style.configure('TButton', font=('Helvetica', 14), padding=[15, 8], relief='raised', background='#007BFF', foreground='white')
        style.configure('TFrame', background='white')
        
        self.tab_control = ttk.Notebook(root)
        
        # Defined scripts and appropriate images
        game_modes = [
            ("CGOL.py", "Conway's Game of Life (Predator vs Prey)", "wolf.png", "mouse.png",
             "• Predators (Wolves) vs Mice (Prey)\n" + 
             "\n" +
             "   - Place mice by left-clicking on grid normally.\n" + 
             "   - Place wolves by left-clicking on grid while holding down shift.\n" + 
             "   - Both species replicate using Conway's Game of Life rules.\n" + 
             "   - Predators take precedence by being able to 'eat' the Mice and take priority in spawning."),

            ("CGOL_Reward.py", "Conway's Game of Life (Food Supply)", "cheese.png", None,
             "• Builds on Predator vs Prey with additional elements:\n" +
             "\n" +
             "   - Randomly placed food sources (Cheese) for the Mice.\n" + 
             "   - Mice eat cheese by being one block away, triggering a spawning pattern in the grid's corner.\n" + 
             "   - Wolves are rewarded for eating Mice by spawning wolves in the grid's corner.\n" + 
             "   - A relative population bar shows the population of each species."),

            ("CGOL_INFECTION.py", "Conway's Game of Life (Infection)", "virus.png", None,
             "• Enhances Predator vs Prey by adding a punishment mechanism:\n" +
             "\n" +
             "   - A virus/infection attacks when relative populations exceed 70%.\n" +
             "   - This prevents overpopulation and maintains balance."),

            ("CGOL_INFECTION_UNDLESS.py", "Conway's Game of Life (Endless)", "infinity.png", None,
             "• Contains all previous adaptations, however introduces an endless cycle\n" +
             "\n" +
             "   - If the population of a species is fewer than 4, an appropriate moving pattern of 4 of that very species will spawn from the corner of the grid\n" +
             "   - This prevents underpopulation, and allows for recovery following extinction events.")
        ]
        
        # Load and prepare images for tab labels and main content
        self.tab_images = {}  # Cache images to avoid garbage collection issues
        self.main_images = {} # Cache for larger images on main pages
        for script, description, image_file, secondary_image_file, game_info in game_modes:
            self.create_tab(script, description, image_file, secondary_image_file, game_info)
        
        self.tab_control.pack(expand=1, fill="both")

    def create_tab(self, script_name, button_text, image_file, secondary_image_file, game_info):
        tab = ttk.Frame(self.tab_control)
        
        # Load and prepare the smaller image for tab labels
        tab_image = Image.open(image_file)
        tab_image = tab_image.resize((30, 30), Image.Resampling.LANCZOS)
        tab_photo = ImageTk.PhotoImage(tab_image)
        self.tab_images[script_name] = tab_photo  # Cache image for tab label
        
        # Load and prepare the larger image for main content
        main_image = Image.open(image_file)
        main_image = main_image.resize((100, 100), Image.Resampling.LANCZOS)
        main_photo = ImageTk.PhotoImage(main_image)
        self.main_images[script_name] = main_photo  # Cache image for main content
        
        # Create a frame to hold the button, large image, and game information
        top_frame = tk.Frame(tab, bg='white')
        top_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Create a label for the large image
        label = tk.Label(top_frame, image=main_photo, bg='white')
        label.image = main_photo  # Keep a reference to avoid garbage collection
        label.pack(side=tk.LEFT, padx=10)
        
        # If there is a secondary image, load and display it as well
        if secondary_image_file:
            secondary_image = Image.open(secondary_image_file)
            secondary_image = secondary_image.resize((100, 100), Image.Resampling.LANCZOS)
            secondary_photo = ImageTk.PhotoImage(secondary_image)
            self.main_images[script_name + "_secondary"] = secondary_photo
            secondary_label = tk.Label(top_frame, image=secondary_photo, bg='white')
            secondary_label.image = secondary_photo
            secondary_label.pack(side=tk.LEFT, padx=10)
        
        # Create a stylized button on the tab to run the script
        button = ttk.Button(top_frame, text=f"Start {button_text}", 
                            command=lambda: run_script(script_name), style='TButton')
        button.pack(side=tk.RIGHT, padx=10)

        # Create a text widget for game information with larger font and black text
        info_text = tk.Text(tab, wrap=tk.WORD, height=8, bg='#f0f0f0', font=('Helvetica', 24), bd=0, fg='black')
        info_text.insert(tk.END, game_info)
        info_text.configure(state='disabled', relief='flat')  # Make it read-only and flat
        info_text.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

        # Add the custom label with small image to the tab control
        self.tab_control.add(tab, text='', image=tab_photo, compound="left")
        self.tab_control.tab(tab, text=button_text, image=tab_photo, compound="left")  # Set the tab with the small image next to text

# Create the main window
root = tk.Tk()
app = ScriptLauncherApp(root)

# Bind the closing event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the application
root.mainloop()
