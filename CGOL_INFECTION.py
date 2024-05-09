"""
Overpopulation of a species is punished by a virus that randomly traverses the grid and kills off the 
overpopulated species until balance is restored within the relative population levels.
"""

import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg




class GroupOfMice:
    def __init__(self):
        self.energy = 50  # Common energy for all mice
        self.mice = []
        self.dead = 0

    def add_mouse(self, mouse):
        self.mice.append(mouse)
    
    def delete_mouse(self, mouse):
        if mouse in self.mice:
            self.mice.remove(mouse)
            self.dead = self.dead+1

    def increase_energy(self, amount):
        self.energy += amount

    def decrease_energy(self, amount=2):
        self.energy -= amount
        if self.energy < 0:
            self.energy = 0
            
    def reset(self):
        self.mice = []
        self.dead = 0

class GroupOfWolves:
    def __init__(self):
        self.energy = 80  # Common energy for all wolves
        self.wolves = []
        self.dead = 0

    def add_wolf(self, wolf):
        self.wolves.append(wolf)

    def delete_wolf(self, wolf):
        if wolf in self.wolves:
            self.wolves.remove(wolf)
            self.dead = self.dead+1
    
    def increase_energy(self, amount):
        self.energy += amount

    def decrease_energy(self, amount=2):
        self.energy -= amount
        if self.energy < 0:
            self.energy = 0
    
    def reset(self):
        self.wolves = []
        self.dead = 0

class Virus:
    def __init__(self):
        # Initialize the position and movement direction of the virus
        self.position = (random.randint(0, grid_height - 2), random.randint(0, grid_width - 2))
        self.direction = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])  # Initial random direction
        self.moves_in_current_direction = 0
        self.max_moves_in_direction = 6  # Increase to have longer movement in one direction

    def move_and_attack(self):
        # Decide if it's time to change direction
        if self.moves_in_current_direction >= self.max_moves_in_direction or self.at_edge():
            self.direction = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            self.moves_in_current_direction = 0

        # Calculate new position based on current direction
        new_x = (self.position[0] + self.direction[0]) % (grid_height - 1)
        new_y = (self.position[1] + self.direction[1]) % (grid_width - 1)
        self.position = (new_x, new_y)
        self.moves_in_current_direction += 1
        self.attack()

    def at_edge(self):
        # Check if the virus is at the edge of the grid
        next_x = self.position[0] + self.direction[0]
        next_y = self.position[1] + self.direction[1]
        return not (0 <= next_x < grid_height - 1 and 0 <= next_y < grid_width - 1)

    def attack(self):
        # Attack the 2x2 block around the current position
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for pos in positions:
            x, y = self.position[0] + pos[0], self.position[1] + pos[1]
            if 0 <= x < grid_height and 0 <= y < grid_width:
                if (self.target_species == 'mouse' and isinstance(grid[x][y], Mouse)) or \
                   (self.target_species == 'wolf' and isinstance(grid[x][y], Wolf)):
                    grid[x][y] = None  # Delete the entity as the virus moves over it
                    if isinstance(grid[x][y], Mouse):
                        group_of_mice.delete_mouse(grid[x][y])
                    elif isinstance(grid[x][y],Wolf):
                        group_of_wolves.delete_wolf(grid[x][y])
              
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
canvas_width = 1400 
canvas_height = 600
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

virus_image_path = "virus.png"
virus_original_image = Image.open(virus_image_path)
virus_resized_image = virus_original_image.resize((cell_size, cell_size), Image.Resampling.LANCZOS)
virus_image = ImageTk.PhotoImage(virus_resized_image)

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


def corner_creation(type, new_grid):
    if type == "mouse":
        
        mouse = Mouse()
        mouse1 = Mouse()
        mouse2 = Mouse()
        mouse3 = Mouse()
        mouse4 = Mouse()
        
        group_of_mice.add_mouse(mouse)
        group_of_mice.add_mouse(mouse1)
        group_of_mice.add_mouse(mouse2)
        group_of_mice.add_mouse(mouse3)
        group_of_mice.add_mouse(mouse4)
        
        new_grid[0][2] = mouse1
        new_grid[1][2] = mouse2
        new_grid[2][2] = mouse3
        new_grid[2][1] = mouse4
        new_grid[1][0] = mouse
              
    elif type == "wolf":
        wolf = Wolf()
        wolf1 = Wolf()
        wolf2 = Wolf()
        wolf3 = Wolf()
        wolf4 = Wolf()
        
        group_of_wolves.add_wolf(wolf)
        group_of_wolves.add_wolf(wolf1)
        group_of_wolves.add_wolf(wolf2)
        group_of_wolves.add_wolf(wolf3)
        group_of_wolves.add_wolf(wolf4)
        
        new_grid[0][grid_width-3] = wolf
        new_grid[1][grid_width-3] = wolf1
        new_grid[2][grid_width-3] = wolf2
        new_grid[1][grid_width-1] = wolf3
        new_grid[2][grid_width-2] = wolf4
        
# Function to reset the game
def reset_game():
    global grid, is_game_active, final_count_mice, final_count_wolves
    final_count_wolves = 0
    final_count_mice = 0
    group_of_mice.reset()
    group_of_wolves.reset()
    is_game_active = False
    grid = np.full((grid_height, grid_width), None, dtype=object)
    place_cheese(5)
    draw_grid()
    game_button.config(text="Start Game")

virus = None  # Initial state without a virus

final_count_mice = len(group_of_wolves.wolves)
final_count_wolves = len(group_of_mice.mice)
def update_grid():
    global grid, is_game_active, virus
    global final_count_mice, final_count_wolves
    
    if not root.winfo_exists():
        return
    if not is_game_active:
        return

    # Population checks to possibly spawn or remove the virus
    total_population = final_count_mice + final_count_wolves
    mice_percentage = final_count_mice / total_population if total_population > 0 else 0
    wolves_percentage = final_count_wolves / total_population if total_population > 0 else 0

    # Decide if virus should be spawned or removed based on population thresholds
    if mice_percentage >= 0.7 and (virus is None or virus.target_species != 'mouse'):
        virus = Virus()
        virus.target_species = 'mouse'
    elif wolves_percentage >= 0.7 and (virus is None or virus.target_species != 'wolf'):
        virus = Virus()
        virus.target_species = 'wolf'
    elif virus and mice_percentage < 0.7 and wolves_percentage < 0.7:
        virus = None
        
    final_count_mice = 0
    final_count_wolves = 0

    new_grid = np.empty_like(grid, dtype=object)

    for i in range(grid_height):
        for j in range(grid_width):
            # Makes 3x3 array for and allows for continuity in the grid from left-right & top-bottom:
            # Top-left:     (i-1, j-1)   |  Top:     (i-1, j)   |  Top-right:     (i-1, j+1)
            # Middle-left:  (i, j-1)     |  Center:  (i, j)     |  Middle-right:  (i, j+1)
            # Bottom-left:  (i+1, j-1)   |  Bottom:  (i+1, j)   |  Bottom-right:  (i+1, j+1)
                        
            neighbours = grid[np.ix_([(i-1) % grid_height, i, (i+1) % grid_height], 
                                     [(j-1) % grid_width, j, (j+1) % grid_width])]
            count_mice = np.sum([1 for cell in neighbours.flatten() if isinstance(cell, Mouse)])
            count_wolves = np.sum([1 for cell in neighbours.flatten() if isinstance(cell, Wolf)])
            
            if grid[i][j]!=None:
                    
                    total = np.sum([1 for cell in neighbours.flatten() if isinstance(cell, Mouse) or isinstance(cell, Wolf)]) - 1
                    if isinstance(grid[i][j], Mouse):
                        print(i, " ", j, " :", count_mice)
                        print(i, " ", j, " :", count_wolves)
                        if count_wolves == 3:
                            wolf = Wolf()
                            new_grid[i][j] = wolf  # Mouse is replaced by wolves
                            group_of_wolves.add_wolf(wolf)
                            group_of_wolves.increase_energy(food_value)
                            corner_creation("wolf", new_grid)
                        elif count_mice == 4 or count_mice == 3:
                            new_grid[i][j] = grid[i][j]
                        elif count_mice not in [4, 3]:
                            group_of_mice.delete_mouse(grid[i][j])
                            new_grid[i][j] = None
                    elif isinstance(grid[i][j], Wolf):
                        if count_wolves in [3, 4]:
                            new_grid[i][j] = grid[i][j]
                        elif count_wolves not in [3, 4]:
                            group_of_wolves.delete_wolf(grid[i][j])
                            new_grid[i][j] = None
                        
                    elif isinstance(grid[i][j], Cheese):
                        if (count_mice > 0 and count_wolves ==3) or count_wolves == 3:
                            wolf = Wolf()
                            new_grid[i][j] = wolf
                            new_x = random.randint(0, grid_width - 1)
                            new_y = random.randint(0, grid_height - 1)
                            while grid[new_y][new_x] is not None:  # Ensure the cell is empty before respawning
                                new_x = random.randint(0, grid_width - 1)
                                new_y = random.randint(0, grid_height - 1)
                            new_grid[new_y][new_x] = Cheese()
                            
                            
                        elif count_mice > 0:
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

                                corner_creation("mouse", new_grid) 
                        else:
                                new_grid[i][j] = Cheese()
                    else: 
                        new_grid[i][j] = grid[i][j]


            else: 
                if count_wolves == 3:
                    wolf = Wolf()
                    new_grid[i][j] = wolf
                    group_of_wolves.add_wolf(wolf)
                    group_of_wolves.decrease_energy(birth_energy_loss)
                elif count_mice == 3:
                    mouse = Mouse()
                    new_grid[i][j] = mouse
                    group_of_mice.add_mouse(mouse)
                    group_of_mice.decrease_energy(birth_energy_loss)     

    # If virus exists, move and attack in a 2x2 block
    if virus:
        virus_positions = [(virus.position[0] + dx, virus.position[1] + dy) for dx in (0, 1) for dy in (0, 1)]
        for x, y in virus_positions:
            if 0 <= x < grid_height and 0 <= y < grid_width:
                if (virus.target_species == 'mouse' and isinstance(grid[x][y], Mouse)) or \
                   (virus.target_species == 'wolf' and isinstance(grid[x][y], Wolf)):
                    new_grid[x][y] = None  # Delete the mouse or wolf as the virus moves over it
                    if isinstance(grid[x][y], Mouse):
                        group_of_mice.delete_mouse(grid[x][y])
                    elif isinstance(grid[x][y],Wolf):
                        group_of_wolves.delete_wolf(grid[x][y])

        # Move virus to a new random position within the grid bounds
        # virus.position = (random.randint(0, grid_height - 2), random.randint(0, grid_width - 2))
        virus.move_and_attack()   
        
    for i in range(grid_height):
        for j in range(grid_width):
            if isinstance(new_grid[i][j], Mouse):
                final_count_mice = final_count_mice+1 
            elif isinstance(new_grid[i][j], Wolf):
                final_count_wolves = final_count_wolves+1                                                     

    grid = new_grid
    draw_grid()
    # Commented out graph updates because it was making the process slower and less smooth  
    update_graph()
    group_of_wolves.dead = 0
    group_of_mice.dead = 0
    if is_game_active:
        root.after(100, update_grid)

def draw_energy_bars():
    energy_bar_height = 200
    global final_count_mice, final_count_wolves
    total_population =  final_count_wolves + final_count_mice
    if total_population > 0:
        mice_percentage = final_count_mice / total_population
        wolves_percentage = final_count_wolves / total_population
    else:
        mice_percentage = 0
        wolves_percentage = 0
    
    # Draw mouse energy bar with title and image placeholder
    canvas.create_text(canvas_width - 125, 30, text="Relative Mouse Population", font=('Arial', 16), fill='black')
    canvas.create_rectangle(canvas_width - 150, 50, canvas_width-100, 50 + energy_bar_height,
                            fill='', outline='black')
    canvas.create_rectangle(canvas_width - 150, 50+ energy_bar_height * (1-mice_percentage), canvas_width-100, 50 + energy_bar_height,
                            fill='green', outline='black')
    canvas.create_image(canvas_width - 125, 150, image=mouse_image)  # Mouse image to the side of the bar
    
    # Draw wolf energy bar with title and image placeholder
    canvas.create_text(canvas_width - 125, 330, text="Relative Wolf Population", font=('Arial', 16), fill='black')
    canvas.create_rectangle(canvas_width - 150, 350, canvas_width-100, 350 + energy_bar_height,
                            fill='', outline='black')
    canvas.create_rectangle(canvas_width - 150, 350 + energy_bar_height * (1-wolves_percentage), canvas_width-100, 350 + energy_bar_height,
                            fill='red', outline='black')
    canvas.create_image(canvas_width - 125, 450, image=wolf_image)  # Wolf image to the side of the bar

    
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

    if virus:
        # Draw the 2x2 virus block as four little virus images
        for pos in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            x, y = virus.position[0] + pos[0], virus.position[1] + pos[1]
            canvas.create_image(y * cell_size, x * cell_size, anchor="nw", image=virus_image) 

    # Draw grid lines last so they are on top of other elements
    for i in range(grid_height):
        canvas.create_line(0, i * cell_size, canvas_width - 200, i * cell_size, fill='gray') # Draw horizontal grid lines
    for j in range(grid_width):
        canvas.create_line(j * cell_size, 0, j * cell_size, canvas_height, fill='gray') # Draw vertical grid lines        

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
    
def update_graph():
    # Add current counts to the lists
    if is_game_active:
        
        global final_count_mice, final_count_wolves
    
        print(final_count_wolves, " ", final_count_mice)
        total = final_count_wolves + final_count_mice + 5   #5 is the number of cheese always present on the grid
        wolves_count_graph.append(final_count_wolves) #Number of wolves.
        mice_count_graph.append(final_count_mice) #Number of mice.
        
        dead_wolves_count.append(group_of_wolves.dead) #Number of dead wolves.
        dead_mice_count.append(group_of_mice.dead) #Number of dead mice.
        
        ratio_wolves.append(final_count_wolves/total) #Ratio number of wolves / total
        ratio_mice.append(final_count_mice/total) # Ration number of wolves / total
        
        mice_energy.append(group_of_mice.energy) #Energy of the group of mice
        wolves_energy.append(group_of_wolves.energy) #Energy of the group of wolves
        
        # Clear the previous plot
        plt.clf()
        
        plt.subplot(1, 2, 1)
        plt.plot(wolves_count_graph, label='wolves')
        plt.plot(mice_count_graph, label='mice')
        plt.xlabel('Generation')
        plt.ylabel('Count Alive')
        plt.title('number of wolves and mice at each generation')
        plt.legend()
        
        """
        plt.subplot(2, 2, 2)
        plt.plot(dead_wolves_count, label='wolves')
        plt.plot(dead_mice_count, label='mice')
        plt.xlabel('Generation')
        plt.ylabel('Count Dead')
        plt.title('Number of dead wolves and mice at each generation')
        plt.legend()"""
        
        plt.subplot(1, 2, 2)
        plt.plot(ratio_wolves, label='wolves')
        plt.plot(ratio_mice, label='mice')
        plt.xlabel('Generation')
        plt.ylabel('Ratio')
        plt.title('Ratio Mice:Cheese:Wolves')
        plt.legend()
        """
        plt.subplot(2, 2, 4)
        plt.plot(wolves_energy, label='wolves')
        plt.plot(mice_energy, label='mice')
        plt.xlabel('Generation')
        plt.ylabel('Energy')
        plt.title('Mice and wolves energy over generations')
        plt.legend()"""
        
        plt.tight_layout
        plt.draw()
        
graph_window = tk.Toplevel(root)
graph_window.title("Population Graph")
graph_window.geometry("1200x900")

#Lists to hold metric data
wolves_count_graph = []
mice_count_graph = []
dead_wolves_count = []
dead_mice_count = []
ratio_mice = []
ratio_wolves = []
mice_energy = []
wolves_energy = []

fig, ax = plt.subplots()
graph_canvas = FigureCanvasTkAgg(fig, master=graph_window)
graph_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



canvas.bind("<Button-1>", toggle_cell)

root.mainloop()
