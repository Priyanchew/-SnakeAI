from tkinter import *
import random
import numpy as np
import heapq

GAME_WIDTH = 1500
GAME_HEIGHT = 800
SPEED = 70
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00e9ff"
FOOD_COLOR = "#ff0040"
BACKGROUND_COLOR = "#d6ffed"


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


class Food:

    def __init__(self):

        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def a_star_search(snake, food):
    grid = np.zeros((GAME_WIDTH // SPACE_SIZE, GAME_HEIGHT // SPACE_SIZE), dtype=int)

    for x, y in snake.coordinates:
        grid[x // SPACE_SIZE][y // SPACE_SIZE] = 1

    start = tuple(snake.coordinates[0])
    end = tuple(food.coordinates)

    open_list = [(0, start)]
    came_from = {}
    g_score = {start: 0}

    while open_list:
        current_g, current = heapq.heappop(open_list)

        if current == end:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_x, next_y = current[0] + dx * SPACE_SIZE, current[1] + dy * SPACE_SIZE
            neighbor = (next_x, next_y)

            if 0 <= next_x < GAME_WIDTH and 0 <= next_y < GAME_HEIGHT and grid[next_x // SPACE_SIZE][next_y // SPACE_SIZE] != 1:
                tentative_g = g_score[current] + SPACE_SIZE
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + ((next_x - end[0]) ** 2 + (next_y - end[1]) ** 2) ** 0.5
                    heapq.heappush(open_list, (f_score, neighbor))

    return []


def next_turn(snake, food):
    global direction

    path = a_star_search(snake, food)

    if path:
        next_head_x, next_head_y = path[1]
        x, y = snake.coordinates[0]

        if next_head_x < x:
            direction = 'left'
        elif next_head_x > x:
            direction = 'right'
        elif next_head_y < y:
            direction = 'up'
        elif next_head_y > y:
            direction = 'down'

    move_snake(snake, direction)

    x, y = snake.coordinates[0]

    if check_collisions(snake):
        game_over()
        return

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        canvas.delete(snake.squares[-1])
        del snake.coordinates[-1]
        del snake.squares[-1]

    window.after(SPEED, next_turn, snake, food)



def move_snake(snake, direction):
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

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)


def check_collisions(snake):
    head_x, head_y = snake.coordinates[0]

    for body_part in snake.coordinates[1:]:
        if head_x == body_part[0] and head_y == body_part[1]:
            return True

    if head_x < 0 or head_x >= GAME_WIDTH or head_y < 0 or head_y >= GAME_HEIGHT:
        return True

    return False



def game_over():
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")



window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()