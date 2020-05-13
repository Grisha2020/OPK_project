#!/usr/bin/env python3

import tkinter as tk
import time
import math


class Point:
    x = None
    y = None


class Tank:
    rotate = 0
    sizes: Point = None
    speed: Point = None
    centre: Point = None
    point_1: Point = None
    point_2: Point = None
    point_3: Point = None
    point_4: Point = None


def create_point(x: int, y: int) -> Point:
    point = Point()
    point.x, point.y = x, y
    return point


def create_tank(x: int, y: int, height: int, width: int, speed_x: int, speed_y: int) -> Tank:
    tank = Tank()
    tank.centre = create_point(x, y)
    tank.sizes = create_point(width, height)
    tank.speed = create_point(speed_x, speed_y)
    tank.point_1 = create_point(0, 0)
    tank.point_2 = create_point(0, 0)
    tank.point_3 = create_point(0, 0)
    tank.point_4 = create_point(0, 0)
    points_tank(tank)
    return tank


def points_tank(tank: Tank) -> None:
    lenght = math.hypot(tank.sizes.x, tank.sizes.y)
    start_rotate = math.atan(tank.sizes.x / tank.sizes.y)
    tank.point_1.x, tank.point_1.y = lenght * math.cos(tank.rotate + start_rotate), lenght * math.sin(
        tank.rotate + start_rotate)
    tank.point_2.x, tank.point_2.y = lenght * math.cos(tank.rotate - start_rotate), lenght * math.sin(
        tank.rotate - start_rotate)
    tank.point_3.x, tank.point_3.y = lenght * math.cos(tank.rotate + start_rotate + math.pi), lenght * math.sin(
        tank.rotate + start_rotate + math.pi)
    tank.point_4.x, tank.point_4.y = lenght * math.cos(tank.rotate - start_rotate + math.pi), lenght * math.sin(
        tank.rotate - start_rotate + math.pi)


def rotate(tank: Tank, direction: str) -> None:
    if tank.rotate >= 2 * math.pi:
        tank.rotate -= 2 * math.pi
    elif tank.rotate <= -2 * math.pi:
        tank.rotate += 2 * math.pi
    if direction == "right":
        tank.rotate += math.pi / 180
        points_tank(tank)
    if direction == "left":
        tank.rotate -= math.pi / 180
        points_tank(tank)


def draw_a_tank(tank):
    tank_1 = canvas.create_polygon(tank.centre.x + tank.point_1.x, tank.centre.y + tank.point_1.y,
                                   tank.centre.x + tank.point_2.x, tank.centre.y + tank.point_2.y,
                                   tank.centre.x + tank.point_3.x, tank.centre.y + tank.point_3.y,
                                   tank.centre.x + tank.point_4.x, tank.centre.y + tank.point_4.y,
                                   fill=COLOR_TANK, outline="")
    return tank_1


# def main():
root = tk.Tk()

SCREEN_WIDTH = root.winfo_screenwidth() - 80
SCREEN_HEIGHT = root.winfo_screenheight() - 80

TITLE_Y = 20

FIELD_PADDING = 30
BORDER_WIDTH = 10
TANK_HEIGHT = 10
TANK_WIDTH = 20

FIELD_X = FIELD_PADDING
FIELD_Y = FIELD_PADDING + TITLE_Y
FIELD_WIDTH = SCREEN_WIDTH - FIELD_X - FIELD_PADDING
FIELD_HEIGHT = SCREEN_HEIGHT - FIELD_Y - FIELD_PADDING

TANK_ACCELERATION = 5

COLOR_BORDER = "#808080"
COLOR_FIELD = "#00FF00"
COLOR_TANK = "#FF0000"

root.title("tanks")
root.resizable(False, False)

canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()

text = canvas.create_text(SCREEN_WIDTH / 2, TITLE_Y,
                          text="Use arrows or WASD to accelerate the TANK, use mouse"
                               " to move the TANK, use Esc to exit.")

border = canvas.create_rectangle(FIELD_X, FIELD_Y,
                                 FIELD_X + FIELD_WIDTH, FIELD_Y + FIELD_HEIGHT,
                                 fill=COLOR_BORDER, outline="")

field = canvas.create_rectangle(FIELD_X + BORDER_WIDTH, FIELD_Y + BORDER_WIDTH,
                                FIELD_X + FIELD_WIDTH - BORDER_WIDTH, FIELD_Y +
                                FIELD_HEIGHT - BORDER_WIDTH, fill=COLOR_FIELD, outline="")

tank = create_tank(FIELD_X + FIELD_WIDTH / 2, FIELD_Y + FIELD_HEIGHT / 2, TANK_HEIGHT, TANK_WIDTH, -2, -2)

tank_1 = draw_a_tank(tank)

last_time = None


def process_key(event):
    dsx, dsy = 0, 0

    # event.char - regular symbols
    # event.keysym - special keys
    if event.keysym == "Up" or event.char == "w":
        dsy = -1
    elif event.keysym == "Down" or event.char == "s":
        dsy = 1
    elif event.keysym == "Left" or event.char == "a":
        rotate(tank, "left")
    elif event.keysym == "Right" or event.char == "d":
        rotate(tank, "right")
    elif event.keysym == "Escape":
        root.quit()
        return
    tank.speed.x += TANK_ACCELERATION * dsx
    tank.speed.y += TANK_ACCELERATION * dsy
    if abs(tank.speed.x) > 1000:
        while abs(tank.speed.x) > 1000:
            if tank.speed.x >= 0:
                tank.speed.x -= 10
            else:
                tank.speed.x += 10
    if abs(tank.speed.y) > 1000:
        while abs(tank.speed.y) > 1000:
            if tank.speed.y >= 0:
                tank.speed.y -= 10
            else:
                tank.speed.y += 10


def process_mouse(event):
    global tank_1
    if 0 <= event.x < SCREEN_WIDTH and 0 <= event.y < SCREEN_HEIGHT:
        # Filter out non-canvas clicks.
        tank.centre.x = event.x
        tank.centre.y = event.y
        canvas.delete(tank_1)
        tank_1 = draw_a_tank(tank)


def update_physics():
    global last_time, tank_1
    cur_time = time.time()
    if last_time:
        dt = cur_time - last_time
        dx = tank.speed.x * dt
        dy = tank.speed.y * dt
        tank.centre.x += dx
        tank.centre.y += dy
        tank_max_x = FIELD_X + FIELD_WIDTH - BORDER_WIDTH - max(tank.point_1.x, tank.point_2.x, tank.point_3.x,
                                                                tank.point_4.x)
        tank_max_y = FIELD_Y + FIELD_HEIGHT - BORDER_WIDTH - max(tank.point_1.y, tank.point_2.y, tank.point_3.y,
                                                                 tank.point_4.y)
        tank_min_x = FIELD_X + BORDER_WIDTH + max(tank.point_1.x, tank.point_2.x, tank.point_3.x, tank.point_4.x)
        tank_min_y = FIELD_Y + BORDER_WIDTH + max(tank.point_1.y, tank.point_2.y, tank.point_3.y, tank.point_4.y)
        if not (tank_min_x <= tank.centre.x <= tank_max_x):
            tank.centre.x = max(tank_min_x, min(tank.centre.x, tank_max_x))
            tank.speed.x = 0
        if not (tank_min_y <= tank.centre.y <= tank_max_y):
            tank.centre.y = max(tank_min_y, min(tank.centre.y, tank_max_y))
            tank.speed.y = 0
        canvas.delete(tank_1)
        tank_1 = draw_a_tank(tank)
    last_time = cur_time

    # update physics as frequent as possible
    root.after(50, update_physics)


root.bind("<Key>", process_key)
root.bind("<Button-1>", process_mouse)

update_physics()
root.mainloop()

# if __name__ == "__main__":
#     main()

