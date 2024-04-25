import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import random

class GroupOfMice:
    def __init__(self):
        self.energy = 50  # Common energy for all mice
        self.mice = []

    def add_mouse(self, mouse):
        self.mice.append(mouse)
    
    def delete_mouse(self, mouse):
        if mouse in self.mice:
            self.mice.remove(mouse)

    def increase_energy(self, amount):
        self.energy += amount

    def decrease_energy(self, amount=2):
        self.energy -= amount
        if self.energy < 0:
            self.energy = 0

class GroupOfWolves:
    def __init__(self):
        self.energy = 80  # Common energy for all wolves
        self.wolves = []

    def add_wolf(self, wolf):
        self.wolves.append(wolf)

    def delete_wolf(self, wolf):
        if wolf in self.wolves:
            self.wolves.remove(wolf)
    
    def increase_energy(self, amount):
        self.energy += amount

    def decrease_energy(self, amount=2):
        self.energy -= amount
        if self.energy < 0:
            self.energy = 0
                      
class Mouse:
    def __init__(self):
        self.type = 1  # Mouse type
        
class Wolf:
    def __init__(self):
        self.type = 2  # Wolf type

class Cheese:
    def __init__(self):
        self.type = 3  # Cheese type

#Initialize the Cheese count and the groups of mice and wolves.
cheese_count = 0
group_of_wolves = GroupOfWolves()
group_of_mice = GroupOfMice()
food_value = 10
birth_energy_loss = 0.2

def place_cheese(num_cheese):
    for _ in range(num_cheese):
        x = random.randint(0, grid_width - 1)
        y = random.randint(0, grid_height - 1)
        while grid[y][x] is not None:  # Ensure the cell is empty before placing cheese
            x = random.randint(0, grid_width - 1)
            y = random.randint(0, grid_height - 1)
        grid[y][x] = Cheese()


# Initialise Main Window
root = tk.Tk()
root.title("Conway's Game of Life (Predator vs Prey)")

# General UI Theme Presets
root.configure(bg='light grey')
frame_style = {'bg': 'light grey'}
text_style = {'bg': 'light grey', 'font': ('Arial', 18)}

# Canvas Dimensions
canvas_width = 1400 + 200
canvas_height = 700
cell_size = 28

# Energy Bar Dimensions
energy_bar_width = 4
energy_bar_height = cell_size

# Create Canvas with new dimensions
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='#d0d0d0')
canvas.pack(padx=10, pady=10)

# Grid Initialisation
grid_height = canvas_height // cell_size
grid_width = (canvas_width-200) // cell_size
grid = np.full((grid_height, grid_width), None, dtype=object)

# Import and Resize Images:
mouse_image_path = "mouse.png"
mouse_original_image = Image.open(mouse_image_path)
mouse_resized_image = mouse_original_image.resize((cell_size, cell_size), Image.Resampling.LANCZOS)
mouse_image = ImageTk.PhotoImage(mouse_resized_image)

wolf_image_path = "wolf.png"
wolf_original_image = Image.open(wolf_image_path)
wolf_resized_image = wolf_original_image.resize((cell_size, cell_size), Image.Resampling.LANCZOS)
wolf_image = ImageTk.PhotoImage(wolf_resized_image)

cheese_image_path = "cheese.png"
cheese_original_image = Image.open(cheese_image_path)
cheese_resized_image = cheese_original_image.resize((cell_size, cell_size), Image.Resampling.LANCZOS)
cheese_image = ImageTk.PhotoImage(cheese_resized_image)

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

# Start/Pause/Resume Button
game_button = tk.Button(button_frame, text="Start Game", command=lambda: toggle_game(), **text_style)
game_button.pack(side='left', padx=10)

# Reset Button
reset_button = tk.Button(button_frame, text="Reset Game", command=lambda: reset_game(), **text_style)
reset_button.pack(side='left', padx=10)

# Flag state to control whether game updates
is_game_active = False

# Function to toggle game running state
def toggle_game():
    global is_game_active
    global cheese_count
    is_game_active = not is_game_active
    game_button.config(text="Pause Game" if is_game_active else "Resume Game")
    if is_game_active:
        if cheese_count ==0:
            place_cheese(5)
            cheese_count += 5
            print("cheese placed")
        draw_grid()
        update_grid()


# Function to reset the game
def reset_game():
    global grid, is_game_active
    is_game_active = False
    grid = np.full((grid_height, grid_width), None, dtype=object)
    place_cheese(20)
    draw_grid()
    game_button.config(text="Start Game")

# Update Function for Game of Life Rules:
def update_grid():
    global grid
    if not is_game_active:
        return  
    new_grid = np.empty_like(grid, dtype=object)
    for i in range(grid_height):
        for j in range(grid_width):
            neighbours = grid[max(i-1, 0):min(i+2, grid_height), max(j-1, 0):min(j+2, grid_width)]
            count_mice = np.sum([1 for cell in neighbours.flatten() if isinstance(cell, Mouse)])
            count_wolves = np.sum([1 for cell in neighbours.flatten() if isinstance(cell, Wolf)])
            
            if isinstance(grid[i][j], Mouse):
                # Apply survival rules
                total = np.sum([1 for cell in neighbours.flatten() if isinstance(cell, Mouse) or isinstance(cell, Wolf)]) - 1
                if total in [2, 3]:
                    # Cell survives; if it's a mouse and surrounded by 3 wolves, it becomes a wolf
                    if count_wolves == 3:
                        wolf = Wolf()
                        new_grid[i][j] = wolf  # Mouse is replaced by wolves
                        group_of_wolves.add_wolf(wolf)
                        group_of_wolves.increase_energy(food_value)
                    else:
                        new_grid[i][j] = grid[i][j]
                else:
                    new_grid[i][j] = None  # Cell dies
            elif isinstance(grid[i][j], Wolf):
                # Apply survival rules for wolf
                total = np.sum([1 for cell in neighbours.flatten() if isinstance(cell, Mouse) or isinstance(cell, Wolf)]) - 1
                if total in [2, 3]:
                    new_grid[i][j] = grid[i][j]  # Wolf survives
                else:
                    new_grid[i][j] = None  # Wolf dies
            elif isinstance(grid[i][j], Cheese):
                if count_mice > 0:
                    new_x = random.randint(0, grid_width - 1)
                    new_y = random.randint(0, grid_height - 1)
                    while grid[new_y][new_x] is not None:  # Ensure the cell is empty before respawning
                        new_x = random.randint(0, grid_width - 1)
                        new_y = random.randint(0, grid_height - 1)
                    new_grid[new_y][new_x] = Cheese()
                    mouse = Mouse()
                    new_grid[i][j] = mouse # Mouse eats the cheese
                    group_of_mice.add_mouse(mouse)
                    group_of_mice.increase_energy(food_value)
                    
                else:
                    new_grid[i][j] = Cheese()
            else:
                # Apply birth rules
                if count_wolves == 3:
                    wolf  = Wolf()
                    new_grid[i][j] = wolf  # Birth of a wolf takes precedence
                    group_of_wolves.add_wolf(wolf)
                    group_of_wolves.decrease_energy(birth_energy_loss)
                elif count_mice == 3:
                    mouse = Mouse()
                    new_grid[i][j] = mouse  # Birth of a mouse, only if no wolves
                    group_of_mice.add_mouse(mouse)
                    group_of_mice.decrease_energy(birth_energy_loss)

    grid = new_grid
    draw_grid()
    if is_game_active:
        root.after(100, update_grid)
        
def draw_energy_bars():
    energy_bar_height = 300
    
    # Draw mouse energy bar
    canvas.create_rectangle(canvas_width - 150, 50, canvas_width-100, 50 + energy_bar_height,
                            fill='', outline='black')
    canvas.create_rectangle(canvas_width - 150, 50+ energy_bar_height *(1-group_of_mice.energy/100), canvas_width-100, 50 + energy_bar_height,
                            fill='green', outline='black')
    
    #Draw Wolf energy bar
    canvas.create_rectangle(canvas_width - 150, 400, canvas_width-100, 400 + energy_bar_height,
                            fill='', outline='black')
    canvas.create_rectangle(canvas_width - 150, 400+ energy_bar_height *(1-group_of_wolves.energy/100), canvas_width-100, 400 + energy_bar_height,
                            fill='red', outline='black')
    

    


    

# Drawing the Grid
def draw_grid():
    canvas.delete("all")
    for i in range(grid_height):
        for j in range(grid_width):
            if isinstance(grid[i][j], Mouse):
                canvas.create_image(j*cell_size, i*cell_size, anchor="nw", image=mouse_image)
                
            elif isinstance(grid[i][j], Wolf):    
                canvas.create_image(j*cell_size, i*cell_size, anchor="nw", image=wolf_image)
                
            elif isinstance(grid[i][j], Cheese):  # Draw cheese
                canvas.create_image(j*cell_size, i*cell_size, anchor="nw", image=cheese_image)
        canvas.create_line(0, i*cell_size, canvas_width-200, i*cell_size, fill='gray')  # Draw horizontal grid lines
    for j in range(grid_width + 1):
        canvas.create_line(j*cell_size, 0, j*cell_size, canvas_height, fill='gray')  # Draw vertical grid lines

    draw_energy_bars()

# Cell Placement
def toggle_cell(event):
    x, y = event.x // cell_size, event.y // cell_size
    if event.state & 0x0001:  # Check if Shift key is down
        # Shift + Click - Place or replace with wolf
        if not isinstance(grid[y][x], Wolf):
            wolf = Wolf()
            grid[y][x] = wolf  # Place wolf
            group_of_wolves.add_wolf(wolf)
        else:
            if isinstance(grid[y][x], Wolf):
                group_of_wolves.delete_wolf(grid[y][x])
            grid[y][x] = None
    else:
        # Normal Click - Place or replace with mouse
        if not isinstance(grid[y][x], Mouse):
            mouse = Mouse()
            grid[y][x] = mouse
            group_of_mice.add_mouse(mouse)
        else:
            if isinstance(grid[y][x], Mouse):
                group_of_mice.delete_mouse(grid[y][x])
            grid[y][x] = None
        
    draw_grid()





canvas.bind("<Button-1>", toggle_cell)

root.mainloop()
