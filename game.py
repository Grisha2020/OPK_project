# !/usr/bin/env python3

import tkinter as tk
import time
import math


class Tank:
    rotate = 0
    speed_x = -2
    speed_y = -2
    x = None
    y = None
    x_1 = None
    y_1 = None
    x_2 = None
    y_2 = None
    x_3 = None
    y_3 = None
    x_4 = None
    y_4 = None


def create_tank(x, y) -> Tank:
    tank = Tank()
    tank.x, tank.y = x, y
    tank.x_1, tank.x_2, tank.x_3, tank.x_4 = 20, 20, -20, -20
    tank.y_1, tank.y_2, tank.y_3, tank.y_4 = -10, 10, 10, -10
    return tank


def rotate(tank: Tank, direction: str):  # Скорей всего косяк в поворотах, хотя может быть в изменении скорости
    if tank.rotate >= 2 * math.pi:
        tank.rotate -= 2 * math.pi
    elif tank.rotate <= -2 * math.pi:
        tank.rotate += 2 * math.pi
    if direction == "right":
        tank.rotate += math.pi / 180
        tank.x_1 = math.sqrt(500) * math.cos(tank.rotate+math.atan(1/2))
        tank.x_2 = math.sqrt(500) * math.cos(tank.rotate-math.atan(1/2))
        tank.x_3 = math.sqrt(500) * math.cos(tank.rotate+math.atan(1/2) + math.pi)
        tank.x_4 = math.sqrt(500) * math.cos(tank.rotate-math.atan(1/2) + math.pi)
        tank.y_1 = math.sqrt(500) * math.sin(tank.rotate+math.atan(1/2))
        tank.y_2 = math.sqrt(500) * math.sin(tank.rotate-math.atan(1/2))
        tank.y_3 = math.sqrt(500) * math.sin(tank.rotate+math.atan(1/2) + math.pi)
        tank.y_4 = math.sqrt(500) * math.sin(tank.rotate-math.atan(1/2) + math.pi)
        # if tank.speed_x >= 0:
        #     tank.speed_x = math.sqrt((tank.speed_x * tank.speed_x)+(tank.speed_y * tank.speed_y)) * math.cos(
        #         tank.rotate)
        # else:
        #     tank.speed_x = -math.sqrt((tank.speed_x * tank.speed_x) + (tank.speed_y * tank.speed_y)) * math.cos(
        #         tank.rotate)
        # if tank.speed_y >= 0:
        #     tank.speed_y = math.sqrt((tank.speed_x * tank.speed_x) + (tank.speed_y * tank.speed_y)) * math.sin(
        #         tank.rotate)
        # else:
        #     tank.speed_y = -math.sqrt((tank.speed_x * tank.speed_x) + (tank.speed_y * tank.speed_y)) * math.sin(
        #         tank.rotate)
    if direction == "left":
        tank.rotate -= math.pi / 180
        tank.x_1 = math.sqrt(500) * math.cos(tank.rotate+math.atan(1/2))
        tank.x_2 = math.sqrt(500) * math.cos(tank.rotate-math.atan(1/2))
        tank.x_3 = math.sqrt(500) * math.cos(tank.rotate+math.atan(1/2) + math.pi)
        tank.x_4 = math.sqrt(500) * math.cos(tank.rotate-math.atan(1/2) + math.pi)
        tank.y_1 = math.sqrt(500) * math.sin(tank.rotate+math.atan(1/2))
        tank.y_2 = math.sqrt(500) * math.sin(tank.rotate-math.atan(1/2))
        tank.y_3 = math.sqrt(500) * math.sin(tank.rotate+math.atan(1/2) + math.pi)
        tank.y_4 = math.sqrt(500) * math.sin(tank.rotate-math.atan(1/2) + math.pi)
        # if int(tank.speed_x) >= 0:
        #     tank.speed_x = math.sqrt((tank.speed_x * tank.speed_x) + (tank.speed_y * tank.speed_y)) * math.cos(
        #         tank.rotate)
        # else:
        #     tank.speed_x = -math.sqrt((tank.speed_x * tank.speed_x) + (tank.speed_y * tank.speed_y)) * math.cos(
        #         tank.rotate)
        # if int(tank.speed_y) >= 0:
        #     tank.speed_y = math.sqrt((tank.speed_x * tank.speed_x) + (tank.speed_y * tank.speed_y)) * math.sin(
        #         tank.rotate)
        # else:
        #     tank.speed_y = -math.sqrt((tank.speed_x * tank.speed_x) + (tank.speed_y * tank.speed_y)) * math.sin(
        #         tank.rotate)

last_time = None

def main():
    root = tk.Tk()

    SCREEN_WIDTH = root.winfo_screenwidth() - 80
    SCREEN_HEIGHT = root.winfo_screenheight() - 80

    TITLE_Y = 20

    FIELD_PADDING = 30
    BORDER_WIDTH = 10

    FIELD_X = FIELD_PADDING
    FIELD_Y = FIELD_PADDING + TITLE_Y
    FIELD_WIDTH = SCREEN_WIDTH - FIELD_X - FIELD_PADDING
    FIELD_HEIGHT = SCREEN_HEIGHT - FIELD_Y - FIELD_PADDING

    TANK_ACCELERATION = 5

    COLOR_BORDER = "#808080"
    COLOR_FIELD = "#00FF00"
    COLOR_TANK = "#FF0FF0"

    tank_max_x = FIELD_X + FIELD_WIDTH - BORDER_WIDTH - math.sqrt(500)
    tank_max_y = FIELD_Y + FIELD_HEIGHT - BORDER_WIDTH - math.sqrt(500)
    tank_min_x = FIELD_X + BORDER_WIDTH + math.sqrt(500)
    tank_min_y = FIELD_Y + BORDER_WIDTH + math.sqrt(500)


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

    tank = create_tank(FIELD_X + FIELD_WIDTH / 2, FIELD_Y + FIELD_HEIGHT / 2)

    tank_1 = canvas.create_polygon(tank.x + tank.x_1, tank.y + tank.y_1, tank.x + tank.x_2, tank.y + tank.y_2,
                                   tank.x + tank.x_3, tank.y + tank.y_3, tank.x + tank.x_4, tank.y + tank.y_4,
                                   fill=COLOR_TANK, outline="")

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
            # canvas.delete(tank_1)
            # tank_1 = canvas.create_polygon(tank.x + tank.x_1, tank.y + tank.y_1, tank.x + tank.x_2, tank.y + tank.y_2,
            #                                tank.x + tank.x_3, tank.y + tank.y_3, tank.x + tank.x_4, tank.y + tank.y_4,
            #                                fill="#808080", outline="")
        elif event.keysym == "Right" or event.char == "d":
            rotate(tank, "right")
            # canvas.delete(tank_1)
            # tank_1 = canvas.create_polygon(tank.x + tank.x_1, tank.y + tank.y_1, tank.x + tank.x_2, tank.y + tank.y_2,
            #                                tank.x + tank.x_3, tank.y + tank.y_3, tank.x + tank.x_4, tank.y + tank.y_4,
            #                                fill=COLOR_TANK, outline="")
        elif event.keysym == "Escape":
            root.quit()
            return
        # global tank_1
        # canvas.delete(tank_1)
        # tank1 = canvas.create_polygon(tank.x + tank.x_1, tank.y + tank.y_1, tank.x + tank.x_2, tank.y + tank.y_2,
        #                               tank.x + tank.x_3, tank.y + tank.y_3, tank.x + tank.x_4, tank.y + tank.y_4,
        #                               fill=COLOR_TANK, outline="")
        if int(tank.speed_x) >= 0:
            tank.speed_x = math.sqrt((tank.speed_x * tank.speed_x) + (tank.speed_y * tank.speed_y)) * math.cos(
                tank.rotate)
        else:
            tank.speed_x = -math.sqrt((tank.speed_x * tank.speed_x) + (tank.speed_y * tank.speed_y)) * math.cos(
                tank.rotate)
        if int(tank.speed_y) >= 0:
            tank.speed_y = math.sqrt((tank.speed_x * tank.speed_x) + (tank.speed_y * tank.speed_y)) * math.sin(
                tank.rotate)
        else:
            tank.speed_y = -math.sqrt((tank.speed_x * tank.speed_x) + (tank.speed_y * tank.speed_y)) * math.sin(
                tank.rotate)
        tank.speed_x += TANK_ACCELERATION * dsx
        tank.speed_y += TANK_ACCELERATION * dsy
        if abs(tank.speed_x) > 1000:
            while abs(tank.speed_x) > 1000:
                if tank.speed_x >= 0:
                    tank.speed_x -= 10
                else:
                    tank.speed_x += 10
        if abs(tank.speed_y) > 1000:
            while abs(tank.speed_y) > 1000:
                if tank.speed_y >= 0:
                    tank.speed_y -= 10
                else:
                    tank.speed_y += 10

    def process_mouse(event):
        if 0 <= event.x < SCREEN_WIDTH and 0 <= event.y < SCREEN_HEIGHT:
            # Filter out non-canvas clicks.
            tank.x = event.x
            tank.y = event.y
            tank_1 = canvas.create_polygon(tank.x + tank.x_1, tank.y + tank.y_1, tank.x + tank.x_2, tank.y + tank.y_2,
                                           tank.x + tank.x_3, tank.y + tank.y_3, tank.x + tank.x_4, tank.y + tank.y_4,
                                           fill=COLOR_TANK, outline="")

    def update_physics():
        global last_time
        cur_time = time.time()
        if last_time:
            dt = cur_time - last_time
            dx = tank.speed_x * dt
            dy = tank.speed_y * dt
            tank.x += dx
            tank.y += dy
            if not (tank_min_x <= tank.x <= tank_max_x):
                tank.x = max(tank_min_x, min(tank.x, tank_max_x))
                tank.speed_x = 0
            if not (tank_min_y <= tank.y <= tank_max_y):
                tank.y = max(tank_min_y, min(tank.y, tank_max_y))
                tank.speed_y = 0

            tank_1 = canvas.create_polygon(tank.x + tank.x_1, tank.y + tank.y_1, tank.x + tank.x_2, tank.y + tank.y_2,
                                           tank.x + tank.x_3, tank.y + tank.y_3, tank.x + tank.x_4, tank.y + tank.y_4,
                                           fill=COLOR_TANK, outline="")

        last_time = cur_time

        # update physics as frequent as possible
        root.after(1, update_physics)

    root.bind("<Key>", process_key)
    root.bind("<Button-1>", process_mouse)

    update_physics()
    root.mainloop()


if __name__ == "__main__":
    main()

