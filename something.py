from tkinter import *
import random
import queue
import numpy as np

GAME_WIDTH = 1500
GAME_HEIGHT = 800
SPEED = 70
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)
    def get_head_coordinates(self):
        return self.coordinates[0]

    def get_body_coordinates(self):
        return self.coordinates[1:]

class Food:

    def __init__(self, snake_coordinates):
        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

            if (x, y) not in snake_coordinates:
                break

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")



def next_turn(snake, food):
    global direction

    x, y = snake.coordinates[0]

    shortest_path_length = find_shortest_path(snake, food)

    # Get the coordinates of the food
    food_x, food_y = food.coordinates

    # Decide the direction based on the shortest path
    if shortest_path_length is not None:
        if x < food_x and direction != "left":
            direction = "right"
        elif x > food_x and direction != "right":
            direction = "left"
        elif y < food_y and direction != "up":
            direction = "down"
        elif y > food_y and direction != "down":
            direction = "up"

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food(snake.coordinates)


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

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")


def find_shortest_path(snake, food):
    grid = np.zeros((GAME_HEIGHT // SPACE_SIZE, GAME_WIDTH // SPACE_SIZE), dtype=int)

    # Mark snake's body as -1 in the grid
    for x, y in snake.get_body_coordinates():
        grid[y // SPACE_SIZE][x // SPACE_SIZE] = -1

    # Create a queue for A* search
    open_list = queue.PriorityQueue()
    start_x, start_y = snake.get_head_coordinates()
    goal_x, goal_y = food.coordinates
    open_list.put((0, (start_x // SPACE_SIZE, start_y // SPACE_SIZE)))

    # Directions for moving (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while not open_list.empty():
        _, (x, y) = open_list.get()

        if x == goal_x // SPACE_SIZE and y == goal_y // SPACE_SIZE:
            path_length = 0
            current_x, current_y = x, y
            while (current_x, current_y) != (start_x // SPACE_SIZE, start_y // SPACE_SIZE):
                path_length += 1
                current_x, current_y = parent[current_x][current_y]
            return path_length

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            if (
                0 <= new_x < len(grid[0])
                and 0 <= new_y < len(grid)
                and grid[new_y][new_x] >= 0  # Not visited or part of the current path
            ):
                grid[new_y][new_x] = -2  # Mark as part of the current path
                cost = abs(new_x - goal_x // SPACE_SIZE) + abs(new_y - goal_y // SPACE_SIZE)
                open_list.put((cost, (new_x, new_y)))
                parent[new_x][new_y] = (x, y)

    return None




window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food(snake.coordinates)
parent = np.zeros((GAME_WIDTH // SPACE_SIZE, GAME_HEIGHT // SPACE_SIZE, 2), dtype=int)

next_turn(snake, food)

window.mainloop()