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
import cv2
import imageio
from tkinter import Toplevel, Label

# Global variable
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
        
        # Sets the theme for thettk widgets
        style = ttk.Style()
        style.theme_use('clam') 
        style.configure('TNotebook.Tab', font=('Helvetica', 10), padding=[30, 12], background='lightblue')
        style.configure('TButton', font=('Helvetica', 14), padding=[15, 8], relief='raised', background='#007BFF', foreground='white')
        style.configure('TFrame', background='white')
        
        self.tab_control = ttk.Notebook(root)
        
        # Defined scripts and appropriate images to accompany them
        # Descriptions for each game mode
        game_modes = [
            ("CGOL.py", "Conway's Game of Life (Predator vs Prey)", "Resources/wolf.png", "Resources/mouse.png",
             "• Predators (Wolves) vs Mice (Prey)\n" + 
             "\n" +
             "   - Place mice by left-clicking on grid normally.\n" + 
             "   - Place wolves by left-clicking on grid while holding down shift.\n" + 
             "   - Both species replicate using Conway's Game of Life rules.\n" + 
             "   - Predators take precedence by being able to 'eat' the Mice and take priority in spawning."),

            ("CGOL_Reward.py", "Conway's Game of Life (Food Supply)", "Resources/cheese.png", None,
             "• Builds on Predator vs Prey with additional elements:\n" +
             "\n" +
             "   - Randomly placed food sources (Cheese) for the Mice.\n" + 
             "   - Mice eat cheese by being one block away, triggering a spawning pattern in the grid's corner.\n" + 
             "   - Wolves are rewarded for eating Mice by spawning wolves in the grid's corner.\n" + 
             "   - A relative population bar shows the population of each species."),

            ("CGOL_INFECTION.py", "Conway's Game of Life (Infection)", "Resources/virus.png", None,
             "• Enhances Predator vs Prey by adding a punishment mechanism:\n" +
             "\n" +
             "   - A virus/infection attacks when relative populations exceed 70%.\n" +
             "   - This prevents overpopulation and maintains balance."),

            ("CGOL_INFECTION_UNDLESS.py", "Conway's Game of Life (Endless)", "Resources/infinity.png", None,
             "• Contains all previous adaptations, however introduces an endless cycle\n" +
             "\n" +
             "   - If the population of a species is fewer than 4, an appropriate moving pattern of 4 of that very species will spawn from the corner of the grid\n" +
             "   - This prevents underpopulation, and allows for recovery following extinction events.")
        ]
        
        # Load and prepare images for tab labels and main content
        self.tab_images = {}  
        self.main_images = {} 
        for script, description, image_file, secondary_image_file, game_info in game_modes:
            self.create_tab(script, description, image_file, secondary_image_file, game_info)
        
        self.tab_control.pack(expand=1, fill="both")

    def create_tab(self, script_name, button_text, image_file, secondary_image_file, game_info):
        tab = ttk.Frame(self.tab_control)
        
        # Load and prepare the smaller image for the tab labels
        tab_image = Image.open(image_file)
        tab_image = tab_image.resize((30, 30), Image.Resampling.LANCZOS)
        tab_photo = ImageTk.PhotoImage(tab_image)
        self.tab_images[script_name] = tab_photo  
        
        # Load and prepare larger image for main canvas page
        main_image = Image.open(image_file)
        main_image = main_image.resize((100, 100), Image.Resampling.LANCZOS)
        main_photo = ImageTk.PhotoImage(main_image)
        self.main_images[script_name] = main_photo  
        
        # Frame to hold the button, large image, and game information
        top_frame = tk.Frame(tab, bg='white')
        top_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Label for the larger image
        label = tk.Label(top_frame, image=main_photo, bg='white')
        label.image = main_photo 
        label.pack(side=tk.LEFT, padx=10)
        
        # If there is a secondary image also display it
        # For the picture for Predator vs Prey in the first game mode
        if secondary_image_file:
            secondary_image = Image.open(secondary_image_file)
            secondary_image = secondary_image.resize((100, 100), Image.Resampling.LANCZOS)
            secondary_photo = ImageTk.PhotoImage(secondary_image)
            self.main_images[script_name + "_secondary"] = secondary_photo
            secondary_label = tk.Label(top_frame, image=secondary_photo, bg='white')
            secondary_label.image = secondary_photo
            secondary_label.pack(side=tk.LEFT, padx=10)
        
        # Creates button to run the respective script
        button = ttk.Button(top_frame, text=f"Start {button_text}", 
                            command=lambda: run_script(script_name), style='TButton')
        button.pack(side=tk.RIGHT, padx=10)

        # Info text widget
        info_text = tk.Text(tab, wrap=tk.WORD, height=8, bg='#f0f0f0', font=('Helvetica', 18), bd=0, fg='black')
        info_text.insert(tk.END, game_info)
        info_text.configure(state='disabled', relief='flat')  # Make it read-only and flat
        info_text.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

        self.tab_control.add(tab, text='', image=tab_photo, compound="left")
        self.tab_control.tab(tab, text=button_text, image=tab_photo, compound="left")  # Set the tab with the small image next to text
        
        # Check if this is the Predator vs Prey tab and add video if so
        if script_name == "CGOL.py":
            self.add_video_to_tab(tab, "Resources/CGOL1_DEMO.mp4")

        # Check if this is the Food Supply Reward tab and add video if so
        if script_name == "CGOL_Reward.py":
            self.add_video_to_tab(tab, "Resources/CGOL2_DEMO_FOODSUPPLY.mp4")

        # Check if this is the Infection tab and add video if so
        if script_name == "CGOL_INFECTION.py":
            self.add_video_to_tab(tab, "Resources/CGOL3_VIRUS.mp4")   

        # Check if this is the Endless tab and add video if so
        if script_name == "CGOL_INFECTION_UNDLESS.py":
            self.add_video_to_tab(tab, "Resources/CGOL4_ENDLESS.mp4")                        
            
          


    def add_video_to_tab(self, tab, video_path):

        video_label = Label(tab, bg='black', width=700, height=800)  # Width x Height
        video_label.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Open the video file using OpenCV
        video_cap = cv2.VideoCapture(video_path)

        def update_frame():
            ret, frame = video_cap.read()
            if not ret:
                # Loop the video
                video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = video_cap.read()
            
            if ret:
                # Convert the image to RGB from BGR
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Resize frame to fit label
                frame = cv2.resize(frame, (700, 350))  # Needs to match the label size

                frame_image = Image.fromarray(frame)
                frame_photo = ImageTk.PhotoImage(image=frame_image)
                video_label.config(image=frame_photo)
                video_label.image = frame_photo
                video_label.after(50, update_frame)  

        update_frame()


# Create the main window
root = tk.Tk()
app = ScriptLauncherApp(root)

# Bind the closing event to the on_closing function
# Stops the game switcher crashing on wassim's laptop
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the application
root.mainloop()