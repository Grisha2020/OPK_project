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


class Gun:
    sizes: Point = None
    tank: Tank = None
    point_near_1: Point = None
    point_near_2: Point = None
    point_further_3: Point = None
    point_further_4: Point = None


class Bullet:
    gun: Gun = None
    centre: Point = None
    rotate = 0
    speed: Point = None
    point_1: Point = None
    point_2: Point = None
    point_3: Point = None
    point_4: Point = None


def create_point(x: int, y: int) -> Point:
    point = Point()
    point.x, point.y = x, y
    return point


def create_tank(x: int, y: int, height: int, width: int, speed_x: int, speed_y: int) -> Tank:
    tank_clone = Tank()
    tank_clone.centre = create_point(x, y)
    tank_clone.sizes = create_point(width, height)
    tank_clone.speed = create_point(speed_x, speed_y)
    tank_clone.point_1 = create_point(0, 0)
    tank_clone.point_2 = create_point(0, 0)
    tank_clone.point_3 = create_point(0, 0)
    tank_clone.point_4 = create_point(0, 0)
    points_tank(tank_clone)
    return tank_clone


def create_gun(height: int, width: int, tank_cl: Tank) -> Gun:
    gun_clone = Gun()
    gun_clone.sizes = create_point(width, height)
    gun_clone.tank = tank_cl
    gun_clone.point_near_1 = create_point(0, 0)
    gun_clone.point_near_2 = create_point(0, 0)
    gun_clone.point_further_3 = create_point(0, 0)
    gun_clone.point_further_4 = create_point(0, 0)
    points_gun(gun_clone)
    return gun_clone


def create_bullet(gun_cl: Gun, speed: int) -> Bullet:
    bullet_clone = Bullet()
    bullet_clone.gun = gun_cl
    bullet_clone.rotate = gun_cl.tank.rotate
    # at the beginning, the center of the bullet should be at the end of the gun
    bullet_clone.centre = create_point(0, 0)
    bullet_clone.centre.x, bullet_clone.centre.y = (gun.tank.centre.x + gun_cl.tank.sizes.y + gun_cl.sizes.y +
                                                    gun_cl.sizes.x) * math.cos(gun_cl.tank.rotate - math.pi / 2),\
                                                   (gun.tank.centre.y + gun_cl.tank.sizes.y + gun_cl.sizes.y +
                                                    gun_cl.sizes.x) * math.sin(gun_cl.tank.rotate - math.pi / 2)
    bullet_clone.speed = create_point(0, 0)
    bullet_clone.speed.x, bullet_clone.speed.y = speed * math.cos(gun_cl.tank.rotate - math.pi / 2), speed * math.sin(
        gun_cl.tank.rotate - math.pi / 2)
    bullet_clone.point_1 = create_point(0, 0)
    bullet_clone.point_2 = create_point(0, 0)
    bullet_clone.point_3 = create_point(0, 0)
    bullet_clone.point_4 = create_point(0, 0)
    points_bullet(bullet_clone)
    return bullet_clone


def points_tank(tank_clone: Tank) -> None:
    lenght = math.hypot(tank_clone.sizes.x, tank_clone.sizes.y)
    start_rotate = math.atan(tank_clone.sizes.x / tank_clone.sizes.y)
    tank_clone.point_1.x, tank_clone.point_1.y = lenght * math.cos(tank_clone.rotate + start_rotate), lenght * math.sin(
        tank_clone.rotate + start_rotate)
    tank_clone.point_2.x, tank_clone.point_2.y = lenght * math.cos(tank_clone.rotate - start_rotate), lenght * math.sin(
        tank_clone.rotate - start_rotate)
    tank_clone.point_3.x, tank_clone.point_3.y = lenght * math.cos(
        tank_clone.rotate + start_rotate + math.pi), lenght * math.sin(tank_clone.rotate + start_rotate + math.pi)
    tank_clone.point_4.x, tank_clone.point_4.y = lenght * math.cos(
        tank_clone.rotate - start_rotate + math.pi), lenght * math.sin(tank_clone.rotate - start_rotate + math.pi)


def points_gun(gun_clone: Gun) -> None:
    lenght_near_points = math.hypot(gun_clone.sizes.y, gun_clone.tank.sizes.x)
    lenght_further_points = math.hypot(gun_clone.sizes.y, gun_clone.sizes.x + gun_clone.tank.sizes.x)
    start_rotate_near = math.atan(gun_clone.sizes.y / gun_clone.tank.sizes.x)
    start_rotate_further = math.atan(gun_clone.sizes.y / (gun_clone.sizes.x + gun_clone.tank.sizes.x))
    gun_clone.point_near_1.x, gun_clone.point_near_1.y = lenght_near_points * math.cos(
        gun_clone.tank.rotate + start_rotate_near - math.pi / 2), lenght_near_points * math.sin(
        gun_clone.tank.rotate + start_rotate_near - math.pi / 2)
    gun_clone.point_near_2.x, gun_clone.point_near_2.y = lenght_near_points * math.cos(
        gun_clone.tank.rotate - start_rotate_near - math.pi / 2), lenght_near_points * math.sin(
        gun_clone.tank.rotate - start_rotate_near - math.pi / 2)
    gun_clone.point_further_3.x, gun_clone.point_further_3.y = lenght_further_points * math.cos(
        gun_clone.tank.rotate - start_rotate_further - math.pi / 2), lenght_further_points * math.sin(
        gun_clone.tank.rotate - start_rotate_further - math.pi / 2)
    gun_clone.point_further_4.x, gun_clone.point_further_4.y = lenght_further_points * math.cos(
        gun_clone.tank.rotate + start_rotate_further - math.pi / 2), lenght_further_points * math.sin(
        gun_clone.tank.rotate + start_rotate_further - math.pi / 2)


def points_bullet(bullet_clone: Bullet) -> None:
    lenght = math.hypot(bullet_clone.gun.sizes.y, bullet_clone.gun.sizes.x)
    start_rotate = math.pi / 4
    bullet_clone.point_1.x, bullet_clone.point_1.y = lenght * math.cos(
        bullet_clone.rotate + start_rotate), lenght * math.sin(bullet_clone.rotate + start_rotate)
    bullet_clone.point_2.x, bullet_clone.point_2.y = lenght * math.cos(
        bullet_clone.rotate + start_rotate), lenght * math.sin(bullet_clone.rotate - start_rotate)
    bullet_clone.point_3.x, bullet_clone.point_3.y = lenght * math.cos(
        bullet_clone.rotate + start_rotate + math.pi), lenght * math.sin(bullet_clone.rotate + start_rotate + math.pi)
    bullet_clone.point_4.x, bullet_clone.point_4.y = lenght * math.cos(
        bullet_clone.rotate + start_rotate + math.pi), lenght * math.sin(bullet_clone.rotate - start_rotate + math.pi)


def rotate(tank_clone: Tank, direction: str) -> None:
    if tank_clone.rotate >= 2 * math.pi:
        tank_clone.rotate -= 2 * math.pi
    elif tank_clone.rotate <= -2 * math.pi:
        tank_clone.rotate += 2 * math.pi
    if direction == "right":
        tank_clone.rotate += 5 * math.pi / 180
        points_tank(tank_clone)
    if direction == "left":
        tank_clone.rotate -= 5 * math.pi / 180
        points_tank(tank_clone)


def speed_change(dspeed: int, tank_clone: Tank):
    speed = math.hypot(abs(tank_clone.speed.x), abs(tank_clone.speed.y))
    # if tank.speed.x >
    tank_clone.speed.x = (speed + TANK_ACCELERATION * dspeed) * math.cos(tank_clone.rotate - math.pi / 2)
    tank_clone.speed.y = (speed + TANK_ACCELERATION * dspeed) * math.sin(tank_clone.rotate - math.pi / 2)
    max_speed = 500
    if abs(tank_clone.speed.x) > max_speed:
        while abs(tank_clone.speed.x) > max_speed:
            if tank_clone.speed.x >= 0:
                tank_clone.speed.x -= 10
            else:
                tank_clone.speed.x += 10
    if abs(tank_clone.speed.y) > max_speed:
        while abs(tank_clone.speed.y) > max_speed:
            if tank_clone.speed.y >= 0:
                tank_clone.speed.y -= 10
            else:
                tank_clone.speed.y += 10


def draw_a_tank(tank_clone, color) -> Tank:
    tank_return = canvas.create_polygon(tank_clone.centre.x + tank_clone.point_1.x,
                                        tank_clone.centre.y + tank_clone.point_1.y,
                                        tank_clone.centre.x + tank_clone.point_2.x,
                                        tank_clone.centre.y + tank_clone.point_2.y,
                                        tank_clone.centre.x + tank_clone.point_3.x,
                                        tank_clone.centre.y + tank_clone.point_3.y,
                                        tank_clone.centre.x + tank_clone.point_4.x,
                                        tank_clone.centre.y + tank_clone.point_4.y, fill=color, outline="")
    return tank_return


def draw_a_gun(gun_clone: Gun, color) -> Gun:
    gun_return = canvas.create_polygon(gun_clone.tank.centre.x + gun_clone.point_near_1.x,
                                       gun_clone.tank.centre.y + gun_clone.point_near_1.y,
                                       gun_clone.tank.centre.x + gun_clone.point_near_2.x,
                                       gun_clone.tank.centre.y + gun_clone.point_near_2.y,
                                       gun_clone.tank.centre.x + gun_clone.point_further_3.x,
                                       gun_clone.tank.centre.y + gun_clone.point_further_3.y,
                                       gun_clone.tank.centre.x + gun_clone.point_further_4.x,
                                       gun_clone.tank.centre.y + gun_clone.point_further_4.y, fill=color, outline="")
    return gun_return


def draw_a_bullet(bullet_clone: Bullet, color) -> Bullet:
    bullet_return = canvas.create_polygon(bullet_clone.centre.x + bullet_clone.point_1.x,
                                          bullet_clone.centre.y + bullet_clone.point_1.y,
                                          bullet_clone.centre.x + bullet_clone.point_2.x,
                                          bullet_clone.centre.y + bullet_clone.point_2.y,
                                          bullet_clone.centre.x + bullet_clone.point_3.x,
                                          bullet_clone.centre.y + bullet_clone.point_3.y,
                                          bullet_clone.centre.x + bullet_clone.point_4.x,
                                          bullet_clone.centre.y + bullet_clone.point_4.y, fill=color, outline="")
    return bullet_return


# def main():
root = tk.Tk()

SCREEN_WIDTH = root.winfo_screenwidth() - 66
SCREEN_HEIGHT = root.winfo_screenheight() - 66

TITLE_Y = 20

FIELD_PADDING = 30
BORDER_WIDTH = 10
TANK_HEIGHT = 20
TANK_WIDTH = 40
TOWER_TANK_SIZE = 16
GUN_HEIGHT = 6
GUN_WIDTH = 40

FIELD_X = FIELD_PADDING
FIELD_Y = FIELD_PADDING + TITLE_Y
FIELD_WIDTH = SCREEN_WIDTH - FIELD_X - FIELD_PADDING
FIELD_HEIGHT = SCREEN_HEIGHT - FIELD_Y - FIELD_PADDING

TANK_ACCELERATION = 10
BULLET_SPEED = 500

COLOR_BORDER = "#808080"
COLOR_FIELD = "#00FF00"
COLOR_TANK = "red"
COLOR_TOWER_TANK = "#0000FF"
COLOR_GUN = "blue"
COLOR_BULLET = "#000000"

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

tank = create_tank(FIELD_X + FIELD_WIDTH / 2, FIELD_Y + FIELD_HEIGHT / 2, TANK_HEIGHT, TANK_WIDTH, 0, 0)
tower_tank = create_tank(FIELD_X + FIELD_WIDTH / 2, FIELD_Y + FIELD_HEIGHT / 2, TOWER_TANK_SIZE, TOWER_TANK_SIZE, 0, 0)
gun = create_gun(GUN_HEIGHT, GUN_WIDTH, tower_tank)
bullet = create_bullet(gun, BULLET_SPEED)

tank_1 = draw_a_tank(tank, COLOR_TANK)
tower_tank_1 = draw_a_tank(tower_tank, COLOR_TOWER_TANK)
gun_1 = draw_a_gun(gun, COLOR_GUN)
bullet_1 = draw_a_bullet(bullet, COLOR_BULLET)

last_time = None


def process_key(event):
    dspeed = 0

    # event.char - regular symbols
    # event.keysym - special keys
    if event.keysym == "Up" or event.char == "w":
        dspeed += 1
    elif event.keysym == "Down" or event.char == "s":
        dspeed -= 1
    elif event.keysym == "Left" or event.char == "a":
        rotate(tank, "left")
        rotate(tower_tank, "left")
        points_gun(gun)
    elif event.keysym == "Right" or event.char == "d":
        rotate(tank, "right")
        rotate(tower_tank, "right")
        points_gun(gun)
    elif event.keysym == "Escape":
        root.quit()
        return
    speed_change(dspeed, tank)
    # update_physics()


# def press_w(event):
#     ds = 1
#     speed_change(ds, tank)
#
#
# def press_s(event):
#     ds = -1
#     speed_change(ds, tank)
#
#
# def press_d(event):
#     ds = 0
#     rotate(tank, "right")
#     rotate(tower_tank, "right")
#     speed_change(ds, tank)
#
#
# def press_a(event):
#     ds = 0
#     rotate(tank, "left")
#     rotate(tower_tank, "left")
#     speed_change(ds, tank)
#
#
# def press_esc(event):
#     root.quit()
#     return


def process_mouse(event):
    global tank_1, tower_tank_1, gun_1
    if 0 <= event.x < SCREEN_WIDTH and 0 <= event.y < SCREEN_HEIGHT:
        # Filter out non-canvas clicks.
        tank.centre.x, tower_tank.centre.x = event.x, event.x
        tank.centre.y, tower_tank.centre.y = event.y, event.y
        points_gun(gun)
        canvas.delete(tank_1)
        canvas.delete(tower_tank_1)
        canvas.delete(gun_1)
        tank_1 = draw_a_tank(tank, COLOR_TANK)
        tower_tank_1 = draw_a_tank(tower_tank, COLOR_TOWER_TANK)
        gun_1 = draw_a_gun(gun, COLOR_GUN)


def process_shot(event):
    global bullet_1
    canvas.delete(bullet_1)
    time.sleep(1)
    bullet_1 = draw_a_bullet(bullet, COLOR_BULLET)
    # a = canvas.create_rectangle(50, 50, 100, 100, fill='red')
    # canvas.create_line(10, 10, 190, 50)


def update_physics():
    global last_time, tank_1, tower_tank_1, gun_1
    cur_time = time.time()
    if last_time:
        dt = cur_time - last_time
        dx_tank = tank.speed.x * dt
        dy_tank = tank.speed.y * dt
        # dx_bullet = bullet.speed.x * dt
        # dy_bullet = bullet.speed.y * dt

        tank.centre.x += dx_tank
        tank.centre.y += dy_tank
        tower_tank.centre.x += dx_tank
        tower_tank.centre.y += dy_tank
        # bullet.centre.x += dx_bullet
        # bullet.centre.y += dy_bullet
        # points_bullet(bullet)

        tank_max_x = FIELD_X + FIELD_WIDTH - BORDER_WIDTH - max(tank.point_1.x, tank.point_2.x, tank.point_3.x,
                                                                tank.point_4.x)
        tank_max_y = FIELD_Y + FIELD_HEIGHT - BORDER_WIDTH - max(tank.point_1.y, tank.point_2.y, tank.point_3.y,
                                                                 tank.point_4.y)
        tank_min_x = FIELD_X + BORDER_WIDTH + max(tank.point_1.x, tank.point_2.x, tank.point_3.x, tank.point_4.x)
        tank_min_y = FIELD_Y + BORDER_WIDTH + max(tank.point_1.y, tank.point_2.y, tank.point_3.y, tank.point_4.y)
        if not (tank_min_x <= tank.centre.x <= tank_max_x):
            tank.centre.x = max(tank_min_x, min(tank.centre.x, tank_max_x))
            tower_tank.centre.x = tank.centre.x
            points_gun(gun)
            tank.speed.x = 0
        if not (tank_min_y <= tank.centre.y <= tank_max_y):
            tank.centre.y = max(tank_min_y, min(tank.centre.y, tank_max_y))
            tower_tank.centre.y = tank.centre.y
            points_gun(gun)
            tank.speed.x = 0
        canvas.delete(tank_1)
        canvas.delete(tower_tank_1)
        canvas.delete(gun_1)
        # canvas.delete(bullet_1)
        tank_1 = draw_a_tank(tank, COLOR_TANK)
        tower_tank_1 = draw_a_tank(tower_tank, COLOR_TOWER_TANK)
        gun_1 = draw_a_gun(gun, COLOR_GUN)
        # bullet_1 = draw_a_bullet(bullet, COLOR_BULLET)
    last_time = cur_time
    # update physics as frequent as possible
    root.after(16, update_physics)


root.bind("<Key>", process_key)
# root.bind("<w>", press_w)
# root.bind("<s>", press_s)
# root.bind("<d>", press_d)
# root.bind("<a>", press_a)
# root.bind("<Escape>", press_esc)
root.bind("<v>", process_shot)
root.bind("<Button-1>", process_mouse)

update_physics()
root.mainloop()

# if __name__ == "__main__":
#     main()

