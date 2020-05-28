#!/usr/bin/env python3

import tkinter as tk
import time
import math


class Point:
    x = None
    y = None


class Rectangle:
    centre: Point = None
    height = None
    width = None
    rotate = None
    point_1: Point = None
    point_2: Point = None
    point_3: Point = None
    point_4: Point = None


class Tank:
    rotate = 0
    sizes: Point = None
    speed: Point = None
    centre: Point = None
    rectangle: Rectangle = None


class Gun:
    sizes: Point = None
    tank: Tank = None
    rectangle: Rectangle = None


class Bullet:
    gun: Gun = None
    centre: Point = None
    rotate = 0
    speed: Point = None
    rectangle: Rectangle = None


def create_point(x: int, y: int) -> Point:
    point = Point()
    point.x, point.y = x, y
    return point


def create_rectangle(centre: Point, height: int, width: int, rotate_r) -> Rectangle:
    rectangle = Rectangle()
    rectangle.centre = centre
    rectangle.height = height
    rectangle.width = width
    rectangle.rotate = rotate_r
    rectangle.point_1 = create_point(0, 0)
    rectangle.point_2 = create_point(0, 0)
    rectangle.point_3 = create_point(0, 0)
    rectangle.point_4 = create_point(0, 0)
    points_rectangle(rectangle)
    return rectangle


def points_rectangle(rectangle: Rectangle) -> None:
    lenght = math.hypot(rectangle.height, rectangle.width)
    start_rotate = math.atan(rectangle.height / rectangle.width)
    pi = math.pi
    rectangle.point_1.x, rectangle.point_1.y = lenght * math.cos(rectangle.rotate + start_rotate), lenght * math.sin(
        rectangle.rotate + start_rotate)
    rectangle.point_2.x, rectangle.point_2.y = lenght * math.cos(rectangle.rotate - start_rotate), lenght * math.sin(
        rectangle.rotate - start_rotate)
    rectangle.point_3.x, rectangle.point_3.y = lenght * math.cos(
        rectangle.rotate + start_rotate + pi), lenght * math.sin(rectangle.rotate + start_rotate + pi)
    rectangle.point_4.x, rectangle.point_4.y = lenght * math.cos(
        rectangle.rotate - start_rotate + pi), lenght * math.sin(rectangle.rotate - start_rotate + pi)


def create_tank(x: int, y: int, height: int, width: int, speed_x: int, speed_y: int) -> Tank:
    tank_clone = Tank()
    tank_clone.centre = create_point(x, y)
    tank_clone.sizes = create_point(width, height)
    tank_clone.speed = create_point(speed_x, speed_y)
    tank_clone.rectangle = create_rectangle(tank_clone.centre, height, width, tank_clone.rotate)
    return tank_clone


def create_gun(height: int, width: int, tank_tower: Tank) -> Gun:
    pi = math.pi
    gun_clone = Gun()
    gun_clone.sizes = create_point(width, height)
    gun_clone.tank = tank_tower
    re_centre = create_point(0, 0)
    re_centre.x, re_centre.y = gun_clone.tank.centre.x + (gun_clone.tank.sizes.y + gun_clone.sizes.x) * math.cos(
        gun_clone.tank.rotate - pi / 2), gun_clone.tank.centre.y + (
                                       gun_clone.tank.sizes.y + gun_clone.sizes.x) * math.sin(
        gun_clone.tank.rotate - pi / 2)
    gun_clone.rectangle = create_rectangle(re_centre, width, height, gun_clone.tank.rotate)
    return gun_clone


def create_bullet(gun_cl: Gun, speed: int) -> Bullet:
    pi = math.pi
    bullet_clone = Bullet()
    bullet_clone.gun = gun_cl
    bullet_clone.rotate = gun_cl.tank.rotate
    # at the beginning, the center of the bullet should be at the end of the gun
    bullet_clone.centre = create_point(0, 0)
    bullet_clone.centre.x, bullet_clone.centre.y = bullet_clone.gun.rectangle.centre.x + math.hypot(
        bullet_clone.gun.sizes.y, bullet_clone.gun.sizes.x) * math.cos(
        bullet_clone.gun.rectangle.rotate - pi / 2), bullet_clone.gun.rectangle.centre.y + math.hypot(
        bullet_clone.gun.sizes.y, bullet_clone.gun.sizes.x) * math.sin(bullet_clone.gun.rectangle.rotate - pi / 2)
    bullet_clone.speed = create_point(0, 0)
    bullet_clone.speed.x, bullet_clone.speed.y = speed * math.cos(
        bullet_clone.gun.tank.rotate - pi / 2), speed * math.sin(bullet_clone.gun.tank.rotate - pi / 2)
    bullet_clone.rectangle = create_rectangle(bullet_clone.centre, bullet_clone.gun.sizes.y, bullet_clone.gun.sizes.y,
                                              bullet_clone.rotate)
    return bullet_clone


def gun_change(gun_clone: Gun) -> None:
    pi = math.pi
    gun_clone.rectangle.rotate = gun_clone.tank.rotate
    gun_clone.rectangle.centre.x, gun_clone.rectangle.centre.y = \
        gun_clone.tank.centre.x + (gun_clone.tank.sizes.y + gun_clone.sizes.x) * \
        math.cos(gun_clone.tank.rotate - pi / 2), gun_clone.tank.centre.y + \
        (gun_clone.tank.sizes.y + gun_clone.sizes.x) * math.sin(gun_clone.tank.rotate - pi / 2)
    points_rectangle(gun_clone.rectangle)


def bullet_change(bullet_clone: Bullet) -> None:
    pi = math.pi
    bullet_clone.centre.x, bullet_clone.centre.y = bullet_clone.gun.rectangle.centre.x + math.hypot(
        bullet_clone.gun.sizes.y, bullet_clone.gun.sizes.x) * math.cos(
        bullet_clone.gun.rectangle.rotate - pi / 2), bullet_clone.gun.rectangle.centre.y + math.hypot(
        bullet_clone.gun.sizes.y, bullet_clone.gun.sizes.x) * math.sin(bullet_clone.gun.rectangle.rotate - pi / 2)
    bullet_clone.speed.x, bullet_clone.speed.y = BULLET_SPEED * math.cos(
        bullet_clone.gun.tank.rotate - pi / 2), BULLET_SPEED * math.sin(bullet_clone.gun.tank.rotate - pi / 2)
    bullet_clone.rotate = bullet_clone.gun.tank.rotate
    bullet_clone.rectangle.rotate = bullet_clone.rotate


def rotate_tank(tank_clone: Tank, direction: str) -> None:
    pi = math.pi
    if tank_clone.rotate >= 2 * pi:
        tank_clone.rotate -= 2 * pi
        tank_clone.rectangle.rotate -= 2 * pi
    elif tank_clone.rotate <= -2 * pi:
        tank_clone.rotate += 2 * pi
        tank_clone.rectangle.rotate += 2 * pi
    rotate_change = 5
    if direction == "right":
        tank_clone.rotate += rotate_change * pi / 180
        tank_clone.rectangle.rotate += rotate_change * pi / 180
        points_rectangle(tank_clone.rectangle)
    if direction == "left":
        tank_clone.rotate -= rotate_change * pi / 180
        tank_clone.rectangle.rotate -= rotate_change * pi / 180
        points_rectangle(tank_clone.rectangle)


def speed_change(dspeed: int, tank_clone: Tank):
    speed = math.hypot(abs(tank_clone.speed.x), abs(tank_clone.speed.y))
    pi = math.pi
    tank_clone.speed.x = (speed + TANK_ACCELERATION * dspeed) * math.cos(tank_clone.rotate - pi / 2)
    tank_clone.speed.y = (speed + TANK_ACCELERATION * dspeed) * math.sin(tank_clone.rotate - pi / 2)
    max_speed = 400
    acceleration = 10
    if abs(tank_clone.speed.x) > max_speed:
        while abs(tank_clone.speed.x) > max_speed:
            if tank_clone.speed.x >= 0:
                tank_clone.speed.x -= acceleration
            else:
                tank_clone.speed.x += acceleration
    if abs(tank_clone.speed.y) > max_speed:
        while abs(tank_clone.speed.y) > max_speed:
            if tank_clone.speed.y >= 0:
                tank_clone.speed.y -= acceleration
            else:
                tank_clone.speed.y += acceleration


def draw_a_object(object_1, color) -> Tank:
    object_return = canvas.create_polygon(object_1.rectangle.centre.x + object_1.rectangle.point_1.x,
                                          object_1.rectangle.centre.y + object_1.rectangle.point_1.y,
                                          object_1.rectangle.centre.x + object_1.rectangle.point_2.x,
                                          object_1.rectangle.centre.y + object_1.rectangle.point_2.y,
                                          object_1.rectangle.centre.x + object_1.rectangle.point_3.x,
                                          object_1.rectangle.centre.y + object_1.rectangle.point_3.y,
                                          object_1.rectangle.centre.x + object_1.rectangle.point_4.x,
                                          object_1.rectangle.centre.y + object_1.rectangle.point_4.y, fill=color,
                                          outline="")
    return object_return


# def main():
root = tk.Tk()

SCREEN_WIDTH = root.winfo_screenwidth() - 66
SCREEN_HEIGHT = root.winfo_screenheight() - 66

TITLE_Y = 20

FIELD_PADDING = 30
BORDER_WIDTH = 10
TANK_WIDTH = 20
TANK_HEIGHT = 40
TOWER_TANK_SIZE = 16
GUN_HEIGHT = 6
GUN_WIDTH = 20

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
COLOR_BULLET = "black"

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

tank_1 = draw_a_object(tank, COLOR_TANK)
tower_tank_1 = draw_a_object(tower_tank, COLOR_TOWER_TANK)
gun_1 = draw_a_object(gun, COLOR_GUN)
bullet_1 = draw_a_object(bullet, COLOR_BULLET)
flag_for_bullet = True

last_time = None


def process_key(event):
    dspeed = 0

    # event.char - regular symbols
    # event.keysym - special keys
    if event.keysym == "Up" or event.char == "w" or event.char == "ц":
        dspeed += 1
    elif event.keysym == "Down" or event.char == "s" or event.char == "ы":
        dspeed -= 1
    elif event.keysym == "Left" or event.char == "a" or event.char == "ф":
        rotate_tank(tank, "left")
        rotate_tank(tower_tank, "left")
        gun_change(gun)
    elif event.keysym == "Right" or event.char == "d" or event.char == "в":
        rotate_tank(tank, "right")
        rotate_tank(tower_tank, "right")
        gun_change(gun)
    elif event.keysym == "Escape":
        root.quit()
        return
    speed_change(dspeed, tank)


def process_mouse(event):
    global tank_1, tower_tank_1, gun_1
    if 0 <= event.x < SCREEN_WIDTH and 0 <= event.y < SCREEN_HEIGHT:
        # Filter out non-canvas clicks.
        tank.centre.x, tower_tank.centre.x = event.x, event.x
        tank.centre.y, tower_tank.centre.y = event.y, event.y
        gun_change(gun)
        canvas.delete(tank_1)
        canvas.delete(tower_tank_1)
        canvas.delete(gun_1)
        tank_1 = draw_a_object(tank, COLOR_TANK)
        tower_tank_1 = draw_a_object(tower_tank, COLOR_TOWER_TANK)
        gun_1 = draw_a_object(gun, COLOR_GUN)


def process_shot(event):
    global bullet_1, bullet, flag_for_bullet
    canvas.delete(bullet_1)
    bullet_change(bullet)
    bullet_1 = draw_a_object(bullet, COLOR_BULLET)
    flag_for_bullet = True

 
def process_rotate_tower(event):  # Криво работает поворот башни
    global tower_tank_1, gun_1
    if event.y - tower_tank.centre.y != 0:
        angle = math.atan((event.x - tower_tank.centre.x) / (event.y - tower_tank.centre.y))
    else:
        angle = 0
    pi = math.pi
    angle_change = 2
    if tower_tank.rotate >= 2 * pi:
        tower_tank.rotate -= 2 * pi
    if tower_tank.rotate <= -2 * pi:
        tower_tank.rotate += 2 * pi
    if gun.rectangle.rotate >= 2 * pi:
        gun.rectangle.rotate -= 2 * pi
    if gun.rectangle.rotate <= -2 * pi:
        gun.rectangle.rotate += 2 * pi
    if tower_tank.rotate <= angle:
        tower_tank.rotate -= angle_change * pi / 180
        tower_tank.rectangle.rotate -= angle_change * math.pi / 180
    if tower_tank.rotate > angle:
        tower_tank.rotate += angle_change * pi / 180
        tower_tank.rectangle.rotate += angle_change * math.pi / 180
    canvas.delete(tower_tank_1)
    points_rectangle(tower_tank.rectangle)
    tower_tank_1 = draw_a_object(tower_tank, COLOR_TOWER_TANK)


def update_physics():
    global last_time, tank_1, tower_tank_1, gun_1, bullet_1, flag_for_bullet
    cur_time = time.time()
    if last_time:
        dt = cur_time - last_time
        dx_tank = tank.speed.x * dt
        dy_tank = tank.speed.y * dt

        dx_bullet = bullet.speed.x * dt
        dy_bullet = bullet.speed.y * dt

        tank.centre.x += dx_tank
        tank.centre.y += dy_tank
        tower_tank.centre.x += dx_tank
        tower_tank.centre.y += dy_tank

        bullet.centre.x += dx_bullet
        bullet.centre.y += dy_bullet
        points_rectangle(bullet.rectangle)

        bullet_max_x = FIELD_X + FIELD_WIDTH - BORDER_WIDTH - max(bullet.rectangle.point_1.x,
                                                                  bullet.rectangle.point_2.x,
                                                                  bullet.rectangle.point_3.x,
                                                                  bullet.rectangle.point_4.x)
        bullet_max_y = FIELD_Y + FIELD_HEIGHT - BORDER_WIDTH - max(bullet.rectangle.point_1.y,
                                                                   bullet.rectangle.point_2.y,
                                                                   bullet.rectangle.point_3.y,
                                                                   bullet.rectangle.point_4.y)
        bullet_min_x = FIELD_X + BORDER_WIDTH + max(bullet.rectangle.point_1.x, bullet.rectangle.point_2.x,
                                                    bullet.rectangle.point_3.x, bullet.rectangle.point_4.x)
        bullet_min_y = FIELD_Y + BORDER_WIDTH + max(bullet.rectangle.point_1.y, bullet.rectangle.point_2.y,
                                                    bullet.rectangle.point_3.y, bullet.rectangle.point_4.y)

        if not (bullet_min_x <= bullet.centre.x <= bullet_max_x):
            canvas.delete(bullet_1)
            flag_for_bullet = False
        if not (bullet_min_y <= bullet.centre.y <= bullet_max_y):
            canvas.delete(bullet_1)
            flag_for_bullet = False

        tank_max_x = FIELD_X + FIELD_WIDTH - BORDER_WIDTH - max(tank.rectangle.point_1.x, tank.rectangle.point_2.x,
                                                                tank.rectangle.point_3.x, tank.rectangle.point_4.x)
        tank_max_y = FIELD_Y + FIELD_HEIGHT - BORDER_WIDTH - max(tank.rectangle.point_1.y, tank.rectangle.point_2.y,
                                                                 tank.rectangle.point_3.y, tank.rectangle.point_4.y)
        tank_min_x = FIELD_X + BORDER_WIDTH + max(tank.rectangle.point_1.x, tank.rectangle.point_2.x,
                                                  tank.rectangle.point_3.x, tank.rectangle.point_4.x)
        tank_min_y = FIELD_Y + BORDER_WIDTH + max(tank.rectangle.point_1.y, tank.rectangle.point_2.y,
                                                  tank.rectangle.point_3.y, tank.rectangle.point_4.y)
        if not (tank_min_x <= tank.centre.x <= tank_max_x):
            tank.centre.x = max(tank_min_x, min(tank.centre.x, tank_max_x))
            tower_tank.centre.x = tank.centre.x
            gun_change(gun)
            tank.speed.x = 0
        if not (tank_min_y <= tank.centre.y <= tank_max_y):
            tank.centre.y = max(tank_min_y, min(tank.centre.y, tank_max_y))
            tower_tank.centre.y = tank.centre.y
            gun_change(gun)
            tank.speed.y = 0

        canvas.delete(tank_1)
        canvas.delete(tower_tank_1)
        canvas.delete(gun_1)
        canvas.delete(bullet_1)

        tank_1 = draw_a_object(tank, COLOR_TANK)
        tower_tank_1 = draw_a_object(tower_tank, COLOR_TOWER_TANK)

        gun_change(gun)
        gun_1 = draw_a_object(gun, COLOR_GUN)
        root.title(gun.rectangle.rotate)

        if flag_for_bullet is True:
            bullet_1 = draw_a_object(bullet, COLOR_BULLET)
    last_time = cur_time
    # update physics as frequent as possible
    root.after(16, update_physics)


root.bind("<Key>", process_key)
root.bind("<space>", process_shot)
root.bind("<Button-1>", process_mouse)
root.bind("<Motion>", process_rotate_tower)

update_physics()
root.mainloop()

# if __name__ == "__main__":
#     main()

