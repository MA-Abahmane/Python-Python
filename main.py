#!/usr/bin/env python3

"""
Python-Python
Dive into a sleek Python Snake Game crafted with Python and TKinter.
Guide the serpent, chase apples, and aim for the high score in this
elegantly coded adventure.
"""

import random
import pygame as pg
from tkinter import *


# Constants
WIDTH = 500
HEIGHT = 500
SPEED = 200
SPACE_SIZE = 20
BODY_SIZE = 2
SNAKE = "#FFFF00"
ECDYSIS = 2
BLUE_SNAKE_COLOR = "#0000FF"
BACKGROUND = "#000000"
FOOD_EMOJI = '🍎'

# Global variables
score = 0
direction = 'down'
play_button = None  # Initialize play_button as None

# Initialise pygame mixer
pg.mixer.init()

class Snake:
    def __init__(self):
        """
        Initialize the Snake class.

        Attributes:
        - body_size: Number of squares in the snake's body.
        - coordinates: List of (x, y) coordinates representing the snake's body.
        - squares: List of Tkinter canvas squares representing the snake's body.
        - eaten_balls: Counter for the number of eaten food items.
        """
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []
        self.eaten_balls = 0

        # Initialize snake coordinates and squares
        for _ in range(BODY_SIZE):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE, tag="snake")
            self.squares.append(square)

    def change_color(self, color):
        """
        Change the color of the snake's body squares.

        Parameters:
        - color: The new color for the snake.
        """
        # Change color of snake squares
        for square in self.squares:
            canvas.itemconfig(square, fill=color)

class Food:
    def __init__(self):
        """
        Initialize the Food class.

        Attributes:
        - coordinates: List representing the (x, y) coordinates of the food.
        """
        # Generate random coordinates for food
        x = random.randint(0, (WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]

        # Create oval with the apple emoji
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="#000000", tag="food", width=0.2)

        # Create text at the center of the oval
        canvas.create_text(x + SPACE_SIZE // 2, y + SPACE_SIZE // 2, text=FOOD_EMOJI, font=('Arial', 20), fill="white", tags="food_text")


def next_turn(snake, food):
    """
    Execute the next turn in the game.

    Parameters:
    - snake: An instance of the Snake class.
    - food: An instance of the Food class.
    """
    x, y = snake.coordinates[0]

    # Update coordinates based on direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    # Create a new square for the snake
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        # Handle when snake eats the food
        global score
        score += 1
        snake.eaten_balls += 1

        # Snake skin change (Yellow | Blue)
        if snake.eaten_balls > ECDYSIS:
            snake.change_color(BLUE_SNAKE_COLOR)

        # set and play eating sound
        sound = pg.mixer.Sound('assets/eat.mp3')
        sound.set_volume(1)
        sound.play()

        label.config(text="Points:{}".format(score))
        canvas.delete("food")
        canvas.delete("food_text")
        food = Food()
    else:
        # Remove the last square if the snake didn't eat food
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        # Schedule the next turn after a delay
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    """
    Change the direction of the snake based on user input.

    Parameters:
    - new_direction: The new direction ('left', 'right', 'up', or 'down').
    """
    global direction
    # Change direction if it's a valid move
    if new_direction in ['left', 'right', 'up', 'down']:
        if (new_direction == 'left' and direction != 'right') or \
           (new_direction == 'right' and direction != 'left') or \
           (new_direction == 'up' and direction != 'down') or \
           (new_direction == 'down' and direction != 'up'):
            direction = new_direction


def check_collisions(snake):
    """
    Check for collisions in the game.

    Parameters:
    - snake: An instance of the Snake class.

    Returns:
    - True if there is a collision, False otherwise.
    """
    x, y = snake.coordinates[0]
    # Check if snake collides with walls or itself
    return x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or any(x == body_part[0] and y == body_part[1] for body_part in snake.coordinates[1:])


def game_over():
    """
    Handle the game over scenario.
    """
    # Handle game over scenario
    canvas.delete(ALL)
    canvas.create_text(WIDTH / 2, HEIGHT / 3, font=('consolas', 70),
                       text="GAME OVER", fill="red", tag="gameover")

    # set and play eating sound
    sound = pg.mixer.Sound('assets/gameover.wav')
    sound.set_volume(1)
    sound.play()
    
    global play_button
    play_button = Button(window, text="READY?", font=('consolas', 20), command=retry_game, border=5, width=8, relief='flat')
    play_button.place(relx=0.5, rely=0.6, anchor=CENTER)


def retry_game():
    """
    Retry the game after game over.
    """
    # Retry the game after game over
    play_button.destroy()
    global score, direction, snake, food
    score = 0
    direction = 'down'
    label.config(text="Points:{}".format(score))
    canvas.delete("all")
    snake = Snake()
    food = Food()
    next_turn(snake, food)


def play():
    """
    Start the game by initializing the snake and food after pressing the PLAY button.
    """
    # Play background music
    music_num = random.randint(1, 5)
    print(music_num)
    pg.mixer.music.load(f"assets/music{music_num}.mp3")
    pg.mixer.music.set_volume(0.25)
    pg.mixer.music.play(-1)
    # Start the game by destroying the play button and initializing snake and food
    play_button.destroy()
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    next_turn(snake, food)


# Tkinter initialization
window = Tk()
window.wm_iconbitmap('assets/py.ico')
window.title("Python Snake Game")

label = Label(window, text="Points:{}".format(score), font=('consolas', 20))
label.pack()

canvas = Canvas(window, bg=BACKGROUND, height=HEIGHT, width=WIDTH)
canvas.pack()

window.update()

# Adjust the window geometry based on screen size
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Display the 'Python Python' title
canvas.create_text((WIDTH / 3) - 29, HEIGHT / 3, font=('consolas', 50, 'bold'),
                   text="Python", fill="yellow", tag="title")
canvas.create_text((WIDTH / 3) * 2 + 29, HEIGHT / 3, font=('consolas', 50, 'bold'),
                   text="Python", fill="blue", tag="title")

# Create Play button
play_button = Button(window, text="PLAY", font=('consolas', 20), command=play, border=7, width=10, relief='flat')
play_button.place(relx=0.5, rely=0.6, anchor=CENTER)

# Start the Tkinter main loop
window.mainloop()
