#!/usr/bin/env python3

from tkinter import *
import random

# Constants
WIDTH = 500
HEIGHT = 500
SPEED = 200
SPACE_SIZE = 20
BODY_SIZE = 2
SNAKE = "#FFFF00"
FOOD_COLOR_THRESHOLD = 2
BLUE_SNAKE_COLOR = "#0000FF"
BACKGROUND = "#000000"
FOOD_EMOJI = '🍎'

# Global variables
score = 0
direction = 'down'
play_button = None  # Initialize play_button as None

class Snake:
    def __init__(self):
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []
        self.eaten_balls = 0

        for _ in range(BODY_SIZE):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE, tag="snake")
            self.squares.append(square)

    def change_color(self, color):
        for square in self.squares:
            canvas.itemconfig(square, fill=color)

class Food:
    def __init__(self):
        x = random.randint(0, (WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]

        # Create oval with the apple emoji
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="#000000", tag="food", width=0.2)

        # Create text at the center of the oval
        canvas.create_text(x + SPACE_SIZE // 2, y + SPACE_SIZE // 2, text=FOOD_EMOJI, font=('Arial', 20), fill="white", tags="food_text")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        snake.eaten_balls += 1

        if snake.eaten_balls > FOOD_COLOR_THRESHOLD:
            snake.change_color(BLUE_SNAKE_COLOR)

        label.config(text="Points:{}".format(score))
        canvas.delete("food")
        canvas.delete("food_text")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction in ['left', 'right', 'up', 'down']:
        if (new_direction == 'left' and direction != 'right') or \
           (new_direction == 'right' and direction != 'left') or \
           (new_direction == 'up' and direction != 'down') or \
           (new_direction == 'down' and direction != 'up'):
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    return x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or any(x == body_part[0] and y == body_part[1] for body_part in snake.coordinates[1:])

def game_over():
    canvas.delete(ALL)
    canvas.create_text(WIDTH / 2, HEIGHT / 3, font=('consolas', 70),
                       text="GAME OVER", fill="red", tag="gameover")
    global play_button
    play_button = Button(window, text="READY?", font=('consolas', 20), command=retry_game, border=5, width=8, height=1)
    play_button.place(relx=0.5, rely=0.6, anchor=CENTER)

def retry_game():
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
    play_button.destroy()
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    next_turn(snake, food)

    # Create Retry button before starting the main loop
    retry_button = Button(window, text="Retry", command=retry_game)
    retry_button.pack()

# Tkinter initialization
window = Tk()
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

# Display Python Python title
canvas.create_text((WIDTH / 3) - 29, HEIGHT / 3, font=('consolas', 50, 'bold'),
                   text="Python", fill="yellow", tag="title")
canvas.create_text((WIDTH / 3) * 2 + 29, HEIGHT / 3, font=('consolas', 50, 'bold'),
                   text="Python", fill="blue", tag="title")

# Create Play button
play_button = Button(window, text="PLAY", font=('consolas', 20), command=play, border=7, width=10)
play_button.place(relx=0.5, rely=0.6, anchor=CENTER)

# Start the Tkinter main loop
window.mainloop()
