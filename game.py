#!/usr/bin/env python3

import tkinter as tk
import time
import math


class Point:
    x = None
    y = None


class Rectangle:
    centre: Point = None
    sizes: Point = None
    rotate = None
    color = None


class Body:
    rectangle: Rectangle = None


class Tower:
    rectangle: Rectangle = None


class Gun:
    rectangle: Rectangle = None


class Tank:
    body: Body = None
    tower: Tower = None
    gun: Gun = None
    speed: Point = None
    polygons = []


class Bullet:
    rectangle: Rectangle = None
    speed: Point = None


def create_point(x, y) -> Point:
    point = Point()
    point.x, point.y = x, y
    return point


def create_rectangle(x_centre: int, y_centre: int, height: int, width: int, start_rotate, color) -> Rectangle:
    rectangle = Rectangle()
    rectangle.centre = create_point(x_centre, y_centre)
    rectangle.sizes = create_point(height, width)
    rectangle.rotate = start_rotate
    rectangle.color = color
    return rectangle


def rotate_rectangle(rectangle: Rectangle, angle_change) -> None:
    if rectangle.rotate > pi:
        rectangle.rotate -= 2 * pi
    if rectangle.rotate <= -pi:
        rectangle.rotate += 2 * pi
    rectangle.rotate += angle_change


def move_rectangle(rectangle: Rectangle, dr: Point) -> None:
    rectangle.centre.x += dr.x
    rectangle.centre.y += dr.y


def points_rectangle(rectangle: Rectangle):
    lenght = math.hypot(rectangle.sizes.x, rectangle.sizes.y)
    start_rotate = math.atan(rectangle.sizes.x / rectangle.sizes.y)
    point_1x, point_1y = lenght * math.cos(rectangle.rotate + start_rotate), lenght * math.sin(
        rectangle.rotate + start_rotate)
    point_2x, point_2y = lenght * math.cos(rectangle.rotate - start_rotate), lenght * math.sin(
        rectangle.rotate - start_rotate)
    point_3x, point_3y = lenght * math.cos(
        rectangle.rotate + start_rotate + pi), lenght * math.sin(rectangle.rotate + start_rotate + pi)
    point_4x, point_4y = lenght * math.cos(
        rectangle.rotate - start_rotate + pi), lenght * math.sin(rectangle.rotate - start_rotate + pi)
    arr_x = [point_1x, point_2x, point_3x, point_4x]
    arr_y = [point_1y, point_2y, point_3y, point_4y]
    return arr_x, arr_y


def intersection(rectangle1: Rectangle, rectangle2: Rectangle) -> bool:  # Не работает для повернутых прямоугольников
    arr_x1, arr_y1 = points_rectangle(rectangle1)
    arr_x2, arr_y2 = points_rectangle(rectangle2)
    for i in range(len(arr_x1)):
        if in_polygon(arr_x1[i], arr_y1[i], arr_x2, arr_y2) == 1:
            return True
    return False


def in_polygon(x, y, xp, yp):  # Не работает для повернутых прямоугольников
    c = 0
    for i in range(len(xp)):
        if (((yp[i] <= y and y < yp[i - 1]) or (yp[i - 1] <= y and y < yp[i])) and (
                x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])):
            c = 1 - 0
    return c


def draw_rectangle(rectangle: Rectangle) -> None:
    arr_x, arr_y = points_rectangle(rectangle)
    object_return = canvas.create_polygon(rectangle.centre.x + arr_x[0],
                                          rectangle.centre.y + arr_y[0],
                                          rectangle.centre.x + arr_x[1],
                                          rectangle.centre.y + arr_y[1],
                                          rectangle.centre.x + arr_x[2],
                                          rectangle.centre.y + arr_y[2],
                                          rectangle.centre.x + arr_x[3],
                                          rectangle.centre.y + arr_y[3], fill=rectangle.color, outline="")
    return object_return


def create_tank(centre_x: int, centre_y: int, height_body: int, width_body: int, color_body: str, height_tower: int,
                width_tower: int, color_tower: str, height_gun: int, width_gun: int, color_gun: str, speed_x: int,
                speed_y: int) -> Tank:
    tank = Tank()
    tank.body = Body()
    tank.body.rectangle = create_rectangle(centre_x, centre_y, height_body, width_body, 0, color_body)
    tank.tower = Tower()
    tank.tower.rectangle = create_rectangle(centre_x, centre_y, height_tower, width_tower, 0, color_tower)
    tank.gun = Gun()
    tank.gun.rectangle = create_rectangle(centre_x, centre_y - height_tower - height_gun, height_gun, width_gun, 0,
                                          color_gun)
    tank.speed = create_point(speed_x, speed_y)
    return tank


def move_tank(tank: Tank, dr: Point) -> None:
    move_rectangle(tank.body.rectangle, dr)
    move_rectangle(tank.tower.rectangle, dr)
    move_rectangle(tank.gun.rectangle, dr)


def rotate_tank(tank: Tank, angle_change) -> None:
    rotate_rectangle(tank.body.rectangle, angle_change)
    rotate_rectangle(tank.tower.rectangle, angle_change)
    rotate_rectangle(tank.gun.rectangle, angle_change)
    tank.gun.rectangle.centre.x, tank.gun.rectangle.centre.y = \
        tank.tower.rectangle.centre.x + (tank.tower.rectangle.sizes.y + tank.gun.rectangle.sizes.x) * \
        math.cos(tank.tower.rectangle.rotate - pi / 2), \
        tank.tower.rectangle.centre.y + (tank.tower.rectangle.sizes.y + tank.gun.rectangle.sizes.x) * \
        math.sin(tank.tower.rectangle.rotate - pi / 2)


def rotate_tower_gun(tank: Tank, angle_change) -> None:
    rotate_rectangle(tank.tower.rectangle, angle_change)
    rotate_rectangle(tank.gun.rectangle, angle_change)
    tank.gun.rectangle.centre.x, tank.gun.rectangle.centre.y = \
        tank.tower.rectangle.centre.x + (tank.tower.rectangle.sizes.y + tank.gun.rectangle.sizes.x) * \
        math.cos(tank.tower.rectangle.rotate - pi / 2), \
        tank.tower.rectangle.centre.y + (tank.tower.rectangle.sizes.y + tank.gun.rectangle.sizes.x) * \
        math.sin(tank.tower.rectangle.rotate - pi / 2)


def speed_change(dspeed: int, tank: Tank):
    speed = math.hypot(abs(tank.speed.x), abs(tank.speed.y))
    tank.speed.x = (speed + TANK_ACCELERATION * dspeed) * math.cos(tank.body.rectangle.rotate - pi / 2)
    tank.speed.y = (speed + TANK_ACCELERATION * dspeed) * math.sin(tank.body.rectangle.rotate - pi / 2)
    max_speed = 400
    acceleration = 10
    if abs(tank.speed.x) > max_speed:
        while abs(tank.speed.x) > max_speed:
            if tank.speed.x >= 0:
                tank.speed.x -= acceleration
            else:
                tank.speed.x += acceleration
    if abs(tank.speed.y) > max_speed:
        while abs(tank.speed.y) > max_speed:
            if tank.speed.y >= 0:
                tank.speed.y -= acceleration
            else:
                tank.speed.y += acceleration


def draw_tank(tank: Tank) -> None:
    if len(tank.polygons) != 0:
        for _ in range(len(tank.polygons)):
            canvas.delete(tank.polygons[0])
            del tank.polygons[0]
    tank.polygons.append(draw_rectangle(tank.body.rectangle))
    tank.polygons.append(draw_rectangle(tank.tower.rectangle))
    tank.polygons.append(draw_rectangle(tank.gun.rectangle))


def create_bullet(tank: Tank, speed: int, color: str) -> Bullet:
    bullet = Bullet()
    x_centre, y_centre = tank.gun.rectangle.centre.x + math.hypot(tank.gun.rectangle.sizes.x,
                                                                  tank.gun.rectangle.sizes.y) * math.cos(
        tank.gun.rectangle.rotate - pi / 2), tank.gun.rectangle.centre.y + math.hypot(tank.gun.rectangle.sizes.x,
                                                                                      tank.gun.rectangle.sizes.y)\
        * math.sin(tank.gun.rectangle.rotate - pi / 2)
    bullet.rectangle = create_rectangle(x_centre, y_centre, tank.gun.rectangle.sizes.y, tank.gun.rectangle.sizes.y,
                                        tank.gun.rectangle.rotate, color)
    bullet.speed = create_point(speed * math.cos(bullet.rectangle.rotate - pi / 2),
                                speed * math.sin(bullet.rectangle.rotate - pi / 2))
    return bullet


def move_bullet(bullet: Bullet, dr: Point) -> None:
    move_rectangle(bullet.rectangle, dr)


def draw_bullet(bullet: Bullet):
    return draw_rectangle(bullet.rectangle)


def process_shot(event):
    global arr_bullet
    bullet = create_bullet(tank1, BULLET_SPEED, COLOR_BULLET)
    arr_bullet.append(bullet)
    arr_bullet_draw.append(draw_bullet(bullet))


def process_key(event):
    dspeed = 0
    # event.char - regular symbols
    # event.keysym - special keys
    if event.keysym == "Up" or event.char == "w" or event.char == "ц":
        dspeed += 1
    elif event.keysym == "Down" or event.char == "s" or event.char == "ы":
        dspeed -= 1
    elif event.keysym == "Left" or event.char == "a" or event.char == "ф":
        rotate_tank(tank1, -5 * pi / 180)
    elif event.keysym == "Right" or event.char == "d" or event.char == "в":
        rotate_tank(tank1, 5 * pi / 180)
    elif event.keysym == "Escape":
        root.quit()
        return
    speed_change(dspeed, tank1)


def process_mouse(event):
    if 0 <= event.x < SCREEN_WIDTH and 0 <= event.y < SCREEN_HEIGHT:
        # Filter out non-canvas clicks.
        move_tank(tank1, create_point(event.x - tank1.body.rectangle.centre.x, event.y - tank1.body.rectangle.centre.y))
        draw_tank(tank1)


def process_rotate_tower(event):  # Криво работает поворот башни
    # move_mouse = create_point(event.x, event.y)
    if event.x - tank1.tower.rectangle.centre.x > 0:
        if event.y - tank1.tower.rectangle.centre.y != 0:
            angle = pi / 2 - math.atan(
                (event.x - tank1.tower.rectangle.centre.x) / (event.y - tank1.tower.rectangle.centre.y))
        else:
            angle = pi / 2
    elif event.x - tank1.tower.rectangle.centre.x > 0:
        if event.y - tank1.tower.rectangle.centre.y != 0:
            angle = -pi / 2 - math.atan(
                (event.x - tank1.tower.rectangle.centre.x) / (event.y - tank1.tower.rectangle.centre.y))
        else:
            angle = -pi / 2
    else:
        angle = 0
    angle_change = 2
    if angle >= 0:
        if angle - pi < tank1.tower.rectangle.rotate < angle:
            rotate_tower_gun(tank1, angle_change * pi / 180)
        elif -pi < tank1.tower.rectangle.rotate < angle - pi or angle < tank1.tower.rectangle.rotate < pi:
            rotate_tower_gun(tank1, -angle_change * pi / 180)
    else:
        if angle < tank1.tower.rectangle.rotate < angle + pi:
            rotate_tower_gun(tank1, angle_change * pi / 180)
        elif -pi < tank1.tower.rectangle.rotate < angle or angle + pi < tank1.tower.rectangle.rotate < pi:
            rotate_tower_gun(tank1, -angle_change * pi / 180)


def update_physics():
    global last_time, tank1, arr_bullet
    cur_time = time.time()
    if last_time:
        dt = cur_time - last_time
        dx_tank = tank1.speed.x * dt
        dy_tank = tank1.speed.y * dt

        move_tank(tank1, create_point(dx_tank, dy_tank))
        try:
            if len(arr_bullet) != 0:
                arr_del_bul = []
                for i in range(len(arr_bullet)):
                    dx_bullet = arr_bullet[i].speed.x * dt
                    dy_bullet = arr_bullet[i].speed.y * dt

                    move_bullet(arr_bullet[i], create_point(dx_bullet, dy_bullet))

                    arr_bul_x, arr_bul_y = points_rectangle(arr_bullet[i].rectangle)
                    bul_max_x = FIELD_X + FIELD_WIDTH - BORDER_WIDTH - max(arr_bul_x)
                    bul_max_y = FIELD_Y + FIELD_HEIGHT - BORDER_WIDTH - max(arr_bul_y)
                    bul_min_x = FIELD_X + BORDER_WIDTH + max(arr_bul_x)
                    bul_min_y = FIELD_Y + BORDER_WIDTH + max(arr_bul_y)
                    if not (bul_min_x <= arr_bullet[i].rectangle.centre.x <= bul_max_x):
                        arr_del_bul.append(i)
                    elif not (bul_min_y <= arr_bullet[i].rectangle.centre.y <= bul_max_y):
                        arr_del_bul.append(i)
                for i in range(len(arr_del_bul)):
                    del arr_bullet[i]
                    canvas.delete(arr_bullet_draw[i])
                    del arr_bullet_draw[i]
                for i in range(len(arr_bullet)):
                    canvas.delete(arr_bullet_draw[0])
                    del arr_bullet_draw[0]
                    arr_bullet_draw.append(draw_bullet(arr_bullet[i]))
        except IndexError:
            """Если кликать мышкой за пределами поля(переносить туда танк), и одновременно стрелять, то патроны
            остаются за пределами поля, и не исчезают
            """
            del arr_bullet[0]
            canvas.delete(arr_bullet_draw[0])
            del arr_bullet_draw[0]

        arr_x, arr_y = points_rectangle(tank1.body.rectangle)
        tank_max_x = FIELD_X + FIELD_WIDTH - BORDER_WIDTH - max(arr_x)
        tank_max_y = FIELD_Y + FIELD_HEIGHT - BORDER_WIDTH - max(arr_y)
        tank_min_x = FIELD_X + BORDER_WIDTH + max(arr_x)
        tank_min_y = FIELD_Y + BORDER_WIDTH + max(arr_y)
        if not (tank_min_x <= tank1.body.rectangle.centre.x <= tank_max_x):
            new_x = -tank1.body.rectangle.centre.x + max(tank_min_x, min(tank1.body.rectangle.centre.x, tank_max_x))
            move_tank(tank1, create_point(new_x, 0))
            tank1.speed.x = 0
        elif not (tank_min_y <= tank1.body.rectangle.centre.y <= tank_max_y):
            new_y = -tank1.body.rectangle.centre.y + max(tank_min_y, min(tank1.body.rectangle.centre.y, tank_max_y))
            move_tank(tank1, create_point(0, new_y))
            tank1.speed.y = 0
    draw_tank(tank1)
    root.title(tank1.gun.rectangle.rotate)

    last_time = cur_time
    # update physics as frequent as possible
    root.after(16, update_physics)


root = tk.Tk()

SCREEN_WIDTH = root.winfo_screenwidth() - 66
SCREEN_HEIGHT = root.winfo_screenheight() - 66

TITLE_Y = 20

FIELD_PADDING = 30
BORDER_WIDTH = 5
TANK_WIDTH = 20
TANK_HEIGHT = 40
TOWER_TANK_SIZE = 16
GUN_HEIGHT = 20
GUN_WIDTH = 6

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

pi = math.pi

arr_bullet = []
arr_bullet_draw = []

root.title("tanks")
root.resizable(False, False)

canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()

text = canvas.create_text(SCREEN_WIDTH / 2, TITLE_Y,
                          text="Use arrows or WASD to accelerate the TANK, use mouse"
                               " to move the TANK, use Esc to exit.")

border = canvas.create_rectangle(FIELD_X, FIELD_Y,
                                 FIELD_X + FIELD_WIDTH, FIELD_Y + FIELD_HEIGHT,
                                 fill=COLOR_FIELD, outline=COLOR_BORDER, width=2 * BORDER_WIDTH)
tank1 = create_tank(FIELD_X + FIELD_WIDTH / 2, FIELD_Y + FIELD_HEIGHT / 2, TANK_HEIGHT, TANK_WIDTH, COLOR_TANK,
                    TOWER_TANK_SIZE, TOWER_TANK_SIZE, COLOR_TOWER_TANK, GUN_HEIGHT, GUN_WIDTH, COLOR_GUN, 0, 0)
draw_tank(tank1)
last_time = None

root.bind("<Key>", process_key)
root.bind("<space>", process_shot)
root.bind("<Button-1>", process_mouse)
root.bind("<Motion>", process_rotate_tower)

update_physics()
root.mainloop()

