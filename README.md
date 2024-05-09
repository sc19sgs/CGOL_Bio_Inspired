# CGOL_Bio_Inspired

## Overview
This project implements Conway's Game of Life (CGOL) integrated with Bio-Inspired Computing principles. It simulates an ecosystem with two types of entities: Mice (Prey) and Wolves (Predators). Users can interactively place these entities on a grid and observe their interactions based on our predefined rules.

## Features
- Interactive grid for placing Mice and Wolves
- Start, Pause, and Reset the simulation
- Custom rules that mimic natural predator-prey dynamics, such as:
* Mode 1: Basic Predator and Prey 

This mode uses two distinct species. Wolves as predators and mice as preys. Both species follows the basic GOL rules, but if a mouse has exactly 3 wolves in its neighbourhood it will die, and a new wolf is created at that position. We also made the cells in the grid wrap around. 

* Mode 2: Conway’s game of life food supply 

This mode is an improvement of the previous one. It keeps the same rules as the basic one with an extra set of rules: 

Population bars for the mice and wolves which acts as our fitness function.  

Mice rewarded for eating a cheese by spawning a new group of mice on the grid  

Wolves rewarded for eating a mouse and are rewarded by spawning a new group of wolves on the grid 

Preventing overpopulation by killing excess wolves which take more than 50% of the grid, killing the wolves are random. 

* Mode 3: Conway’s game of life Infection 

The infection mode adds a virus in addition to the rules in the previous mode, which tries to balance the population. It targets the species which is overpopulated if the population of a species is above 70%, then the virus will target this species. Once the population is below 70%, then the virus will disappear. 

* Mode 4: Conway’s game of life Infection Endless 

This mode also builds upon the previous ones, but the population of any species can’t be 0. This results in infinite predator-prey dynamics, since a minimum of 4 of each species to be present on the grid. Should an extinction event occur, a glider pattern spawns for the affected species. 


### Requirements
- PIL 
- Numpy 
- Tkinter

## Tutorial:
To run this program from a python virtual environment
* Activate your [virtual environment](https://docs.python.org/3/tutorial/venv.html)
* Run ```pip install -r requirements.txt``` to install the necessary dependencies

* Run ```python Game_Modes.py``` to start the application and choose your Game Mode

* Basic Instructions:

1. Place Mice (Prey) in grid and/or Wolves (Predators) using left-click and shift + left-click respectively

2. Press "Start Game" and observe the simulation using our rules

<img width="1425" alt="Screenshot 2024-04-16 at 20 11 37" src="https://github.com/sc19sgs/CGOL_Bio_Inspired/assets/100528174/6332a6e1-fd61-45a6-8eea-81b3924b2cf2">


