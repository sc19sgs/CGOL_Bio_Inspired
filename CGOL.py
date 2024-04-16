import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

# Initialise Main Window
root = tk.Tk()
root.title("Conway's Game of Life (Predator vs Prey)")

# General UI Theme Presets
root.configure(bg='light grey')
frame_style = {'bg': 'light grey'}
text_style = {'bg': 'light grey', 'font': ('Arial', 18)}

# Canvas Dimensions
canvas_width = 1400
canvas_height = 600
cell_size = 28

# Create Canvas with new dimensions
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack(padx=10, pady=10)

# Grid Initialisation
grid_height = canvas_height // cell_size
grid_width = canvas_width // cell_size
grid = np.zeros((grid_height, grid_width), dtype=int)

# Import and Resize Images:
mouse_image_path = "mouse.png"
mouse_original_image = Image.open(mouse_image_path)
mouse_resized_image = mouse_original_image.resize((cell_size, cell_size), Image.Resampling.LANCZOS)
mouse_image = ImageTk.PhotoImage(mouse_resized_image)

wolf_image_path = "wolf.png"
wolf_original_image = Image.open(wolf_image_path)
wolf_resized_image = wolf_original_image.resize((cell_size, cell_size), Image.Resampling.LANCZOS)
wolf_image = ImageTk.PhotoImage(wolf_resized_image)

# Title and Images
title_frame = tk.Frame(root, **frame_style)
title_frame.pack(fill='x', padx=10, pady=5)

# Mouse Image and Label
mouse_label = tk.Label(title_frame, image=mouse_image, **frame_style)
mouse_label.pack(side='left', padx=10)

# Centred Title Label
title_label = tk.Label(title_frame, text="Conway's Game of Life", **text_style)
title_label.pack(side='left', expand=True)

# Wolf Image and Label
wolf_label = tk.Label(title_frame, image=wolf_image, **frame_style)
wolf_label.pack(side='left', padx=10)

# Button Frame
button_frame = tk.Frame(root, **frame_style)
button_frame.pack(fill='x', padx=10, pady=5)

# Start Button
start_button = tk.Button(button_frame, text="Start Game", command=lambda: start_game(), **text_style)
start_button.pack(side='left', padx=10)

# Reset Button
reset_button = tk.Button(button_frame, text="Reset Game", command=lambda: reset_game(), **text_style)
reset_button.pack(side='left', padx=10)

# Flag state to control whether game updates
is_game_active = False

# Function to start the game
def start_game():
    global is_game_active
    is_game_active = True
    update_grid()

# Function to reset the game
def reset_game():
    global grid, is_game_active
    is_game_active = False
    grid = np.zeros((grid_height, grid_width), dtype=int)
    draw_grid()

# Update Function for Game of Life Rules:
def update_grid():
    global grid
    if not is_game_active:
        return    
    new_grid = np.zeros_like(grid)
    for i in range(grid_height):
        for j in range(grid_width):
            neighbours = grid[max(i-1, 0):min(i+2, grid_height), max(j-1, 0):min(j+2, grid_width)]
            count_mice = np.sum(neighbours == 1)
            count_wolves = np.sum(neighbours == 2)
            
            if grid[i][j] != 0:
                # Apply survival rules
                total = np.sum(neighbours == grid[i][j]) - (grid[i][j] != 0)
                if total in [2, 3]:
                    # Cell survives; if it's a mouse and surrounded by 3 wolves, it becomes a wolf
                    if grid[i][j] == 1 and count_wolves == 3:
                        new_grid[i][j] = 2  # Mouse is replaced by wolves
                    else:
                        new_grid[i][j] = grid[i][j]
                else:
                    new_grid[i][j] = 0  # Cell dies
            else:
                # Apply birth rules
                if count_wolves == 3:
                    new_grid[i][j] = 2  # Birth of a wolf takes precedence
                elif count_mice == 3:
                    new_grid[i][j] = 1  # Birth of a mouse, only if no wolves

    grid = new_grid
    draw_grid()
    root.after(100, update_grid)

# Drawing the Grid
def draw_grid():
    canvas.delete("all")
    for i in range(grid_height):
        for j in range(grid_width):
            if grid[i][j] == 1:
                canvas.create_image(j*cell_size, i*cell_size, anchor="nw", image=mouse_image)
            elif grid[i][j] == 2:
                canvas.create_image(j*cell_size, i*cell_size, anchor="nw", image=wolf_image)
        canvas.create_line(0, i*cell_size, canvas_width, i*cell_size, fill='gray')  # Draw horizontal grid lines
    for j in range(grid_width + 1):
        canvas.create_line(j*cell_size, 0, j*cell_size, canvas_height, fill='gray')  # Draw vertical grid lines

# Cell Placement
def toggle_cell(event):
    x, y = event.x // cell_size, event.y // cell_size
    if event.state & 0x0001:  # Check if Shift key is down
        # Shift + Click - Place or replace with wolf
        if grid[y][x] != 2:
            grid[y][x] = 2  # Place wolf
        else:
            grid[y][x] = 0  # Clear cell if it's already a wolf
    else:
        # Normal Click - Place or replace with mouse
        if grid[y][x] != 1:
            grid[y][x] = 1  # Place mouse
        else:
            grid[y][x] = 0  # Clear cell if it's already a mouse
    draw_grid()

canvas.bind("<Button-1>", toggle_cell)

# Running the application
root.mainloop()
