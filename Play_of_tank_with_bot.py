# !/usr/bin/env python3

import tkinter as tk
import time
import math
import random
import Rectangle
import Tank
import Bullet_and_target
import Test_rectangle


class Score:
    value: int = None
    draw_score = None


def draw_rectangle(rectangle: Rectangle.Rectangle) -> None:
    """
    Draws a rectangle at 4 vertices
    :param rectangle:
    :return:
    """
    arr_x, arr_y = Rectangle.points_rectangle(rectangle)
    object_return = canvas.create_polygon(rectangle.centre.x + arr_x[0],
                                          rectangle.centre.y + arr_y[0],
                                          rectangle.centre.x + arr_x[1],
                                          rectangle.centre.y + arr_y[1],
                                          rectangle.centre.x + arr_x[2],
                                          rectangle.centre.y + arr_y[2],
                                          rectangle.centre.x + arr_x[3],
                                          rectangle.centre.y + arr_y[3], fill=rectangle.color, outline="")
    return object_return


def draw_tank(tank: Tank) -> None:
    if len(tank.polygons) != 0:
        for i in range(len(tank.polygons)):
            canvas.delete(tank.polygons[i])
    del tank.polygons = []
    tank.polygons.append(draw_rectangle(tank.body.rectangle))
    tank.polygons.append(draw_rectangle(tank.tower.rectangle))
    tank.polygons.append(draw_rectangle(tank.gun.rectangle))


def draw_bullet(bullet: Bullet_and_target.Bullet):
    return draw_rectangle(bullet.rectangle)


def draw_target(target: Bullet_and_target.Target):
    return draw_rectangle(target.rectangle)


def create_score(value: int, color: str, centre_x: int, centre_y: int, font: str, font_size: int) -> Score:
    score_1 = Score()
    score_1.value = value
    score_1.draw_score = canvas.create_text(centre_x, centre_y, text=value, font=(font, font_size), fill=color)
    return score_1


def change_score(score_1: Score, increase: int) -> None:
    score_1.value += increase
    canvas.itemconfig(score_1.draw_score, text=score_1.value)


def process_shot(event):
    shots(tank1, time_for_bullet)


def shots(tank: Tank.Tank, time_tank):
    global arr_bullet
    if time_tank + TIME_RESPAWN_BULLET < time.time():
        if len(arr_bullet) <= MAXIMUM_NUMBER_OF_BULLET:
            bullet = Bullet_and_target.create_bullet(tank, BULLET_SPEED, COLOR_BULLET)
            arr_bullet.append(bullet)
            arr_bullet_draw.append(draw_bullet(bullet))
            time_tank = time.time()


def process_key(event):
    dspeed = 0
    # event.char - regular symbols
    # event.keysym - special keys
    if event.keysym == "Up" or event.char == "w" or event.char == "ц":
        dspeed += TANK_ACCELERATION
    elif event.keysym == "Down" or event.char == "s" or event.char == "ы":
        dspeed -= TANK_ACCELERATION
    elif event.keysym == "Left" or event.char == "a" or event.char == "ф":
        Tank.rotate_tank(tank1, -5 * pi / 180)
    elif event.keysym == "Right" or event.char == "d" or event.char == "в":
        Tank.rotate_tank(tank1, 5 * pi / 180)
    elif event.keysym == "Escape":
        root.quit()
        return
    Tank.speed_change(dspeed, tank1, MAXIMUM_SPEED)


def mouse_position_memorization(event):
    """
    Remembers mouse coordinates
    :param event:
    :return:
    """
    mouse_position.x, mouse_position.y = event.x, event.y


def process_rotate_tower(mouse: Rectangle.Point, tank: Tank.Tank) -> None:
    """
    The tower with the cannon should be rotated to the coordinates of the mouse, but in some way a problem arises and
     "inversion"
    :param mouse:
    :param tank:
    :return:
    """
    if mouse.x - tank.tower.rectangle.centre.x > 0:
        angle = pi / 2 - math.atan(
            (-mouse.y + tank.tower.rectangle.centre.y) / (mouse.x - tank.tower.rectangle.centre.x))
    elif mouse.x - tank.tower.rectangle.centre.x < 0:
        angle = -pi / 2 - math.atan(
            (-mouse.y + tank.tower.rectangle.centre.y) / (mouse.x - tank.tower.rectangle.centre.x))
    else:
        if mouse.y > tank.tower.rectangle.centre.y:
            angle = pi
        else:
            angle = 0
    angle_change = 6
    if abs(angle - tank.tower.rectangle.rotate) >= angle_change * pi / 180:
        if angle > 0:
            if angle - pi <= tank.tower.rectangle.rotate <= angle:
                Tank.rotate_tower_gun(tank, angle_change * pi / 180)
            elif -pi <= tank.tower.rectangle.rotate <= angle - pi or angle < tank.tower.rectangle.rotate < pi:
                Tank.rotate_tower_gun(tank, -angle_change * pi / 180)
        else:
            if angle <= tank.tower.rectangle.rotate <= angle + pi:
                Tank.rotate_tower_gun(tank, -angle_change * pi / 180)
            elif -pi <= tank.tower.rectangle.rotate <= angle or angle + pi < tank.tower.rectangle.rotate < pi:
                Tank.rotate_tower_gun(tank, angle_change * pi / 180)


def tanks():
    global arr_tanks, time_for_tanks
    if time_for_tanks + TIME_RESPAWN_TANKS < last_time:
        if len(arr_target) < MAXIMUM_NUMBER_OF_TANKS:
            flag_of_tanks = False
            new_point = Rectangle.create_point(0, 0)
            while flag_of_tanks is False:
                new_point.x, new_point.y = \
                    random.randrange(FIELD_X + BORDER_WIDTH + TARGET_WIDTH, FIELD_X +
                                     FIELD_WIDTH - BORDER_WIDTH - TARGET_WIDTH), \
                    random.randrange(FIELD_Y + BORDER_WIDTH + TARGET_HEIGHT, FIELD_Y +
                                     FIELD_HEIGHT - BORDER_WIDTH - TARGET_HEIGHT)
                flag_1 = False
                for i in range(len(arr_target)):
                    if Rectangle.in_rectangle(arr_target[i].rectangle, new_point,
                                              int(math.hypot(TANK_HEIGHT, TANK_WIDTH) + 1)) is True:
                        flag_1 = True
                        break
                if flag_1 is True:
                    continue
                if Rectangle.in_rectangle(tank1.body.rectangle, new_point,
                                          int(math.hypot(TANK_HEIGHT, TANK_WIDTH) + 1)) is True:
                    continue
                flag_of_tanks = True
            arr_tanks.append(
                Tank.create_tank(new_point.x, new_point.y, TANK_HEIGHT, TANK_WIDTH, COLOR_TANKS, TOWER_TANK_SIZE,
                                 TOWER_TANK_SIZE, COLOR_TANKS_TOWER, GUN_HEIGHT, GUN_WIDTH, COLOR_TANKS_GUN,
                                 START_SPEED_TANK_X, START_SPEED_TANK_Y,
                                 START_ROTATE_TANKS[random.randint(0, len(START_ROTATE_TANKS) - 1)]))
            time_for_tanks = last_time


def contact_with_field_boundaries(object_) -> str:
    """
    Checks if an object is out of the field
    :param object_:
    :return:
    """
    arr_x, arr_y = Rectangle.points_rectangle(object_.rectangle)
    max_x = FIELD_X + FIELD_WIDTH - BORDER_WIDTH - max(arr_x)
    max_y = FIELD_Y + FIELD_HEIGHT - BORDER_WIDTH - max(arr_y)
    min_x = FIELD_X + BORDER_WIDTH + max(arr_x)
    min_y = FIELD_Y + BORDER_WIDTH + max(arr_y)
    if not (min_x <= object_.rectangle.centre.x <= max_x):
        return "x"
    elif not (min_y <= object_.rectangle.centre.y <= max_y):
        return "y"
    return "Not touch"


def accommodation_targets() -> None:
    """
    Places targets so that they do not touch the tank and other targets
    :return:
    """
    global time_for_target, last_time
    if time_for_target + TIME_RESPAWN_TARGETS < last_time:
        if len(arr_target) < MAXIMUM_NUMBER_OF_TARGETS:
            flag_of_target = False
            new_point = Rectangle.create_point(0, 0)
            while flag_of_target is False:
                new_point.x, new_point.y = \
                    random.randrange(FIELD_X + BORDER_WIDTH + TARGET_WIDTH, FIELD_X +
                                     FIELD_WIDTH - BORDER_WIDTH - TARGET_WIDTH), \
                    random.randrange(FIELD_Y + BORDER_WIDTH + TARGET_HEIGHT, FIELD_Y +
                                     FIELD_HEIGHT - BORDER_WIDTH - TARGET_HEIGHT)
                flag_1 = False
                for i in range(len(arr_target)):
                    if Rectangle.in_rectangle(arr_target[i].rectangle, new_point, TARGET_WIDTH) is True:
                        flag_1 = True
                        break
                if flag_1 is True:
                    continue
                if Rectangle.in_rectangle(tank1.body.rectangle, new_point, TARGET_WIDTH) is True:
                    continue
                flag_of_target = True
            arr_target.append(
                Bullet_and_target.create_target(new_point.x, new_point.y, TARGET_HEIGHT, TARGET_WIDTH,
                                                ROTATE_TARGETS, COLOR_TARGET))
            arr_target_draw.append(draw_target(arr_target[-1]))
        time_for_target = last_time


def bullets_movement(dt) -> None:
    """
    In addition to the movement of bullets, it checks each bullet for crossing the field boundary
    :param dt:
    :return:
    """
    try:
        if len(arr_bullet) != 0:
            arr_del_bul = []
            for i in range(len(arr_bullet)):
                dx_bullet = arr_bullet[i].speed.x * dt
                dy_bullet = arr_bullet[i].speed.y * dt

                Bullet_and_target.move_bullet(arr_bullet[i], Rectangle.create_point(dx_bullet, dy_bullet))
                touch = contact_with_field_boundaries(arr_bullet[i])
                if touch == "x" or touch == "y":
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
        del arr_bullet[0]
        canvas.delete(arr_bullet_draw[0])
        del arr_bullet_draw[0]


def contact_with_target() -> None:
    """
    There was contact between bullets and targets, also between the tank and targets
    :return:
    """
    global arr_target, arr_bullet, arr_target_draw, arr_bullet_draw
    if len(arr_target) > 0:
        arr_del_bul_1 = []
        arr_del_tar = []
        for i in range(len(arr_target)):
            for j in range(len(arr_bullet)):
                if Rectangle.intersection(arr_target[i].rectangle, arr_bullet[j].rectangle) is True:
                    arr_del_bul_1.append(j)
                    arr_del_tar.append(i)
                    break
        for i in range(len(arr_del_tar)):
            try:
                canvas.delete(arr_target_draw[arr_del_tar[len(arr_del_tar) - i - 1]])
                canvas.delete(arr_bullet_draw[arr_del_bul_1[len(arr_del_tar) - i - 1]])
                del arr_bullet_draw[arr_del_bul_1[len(arr_del_tar) - i - 1]]
                del arr_bullet[arr_del_bul_1[len(arr_del_tar) - i - 1]]
                del arr_target_draw[arr_del_tar[len(arr_del_tar) - i - 1]]
                del arr_target[arr_del_tar[len(arr_del_tar) - i - 1]]
                change_score(score, 1)
            except IndexError:
                continue
        arr_del_tar = []
        for m in range(len(arr_target)):
            if Rectangle.intersection(arr_target[m].rectangle, tank1.body.rectangle) is True:
                arr_del_tar.append(m)
        for _ in range(len(arr_del_tar)):
            canvas.delete(arr_target_draw[arr_del_tar[0]])
            del arr_target[arr_del_tar[0]]
            del arr_target_draw[arr_del_tar[0]]
            change_score(score, 1)


def tank_with_field(tank: Tank.Tank) -> None:
    """
    Did the tank go out of the field
    :param tank:
    :return:
    """
    arr_x, arr_y = Rectangle.points_rectangle(tank.body.rectangle)
    tank_max_x = FIELD_X + FIELD_WIDTH - BORDER_WIDTH - max(arr_x)
    tank_max_y = FIELD_Y + FIELD_HEIGHT - BORDER_WIDTH - max(arr_y)
    tank_min_x = FIELD_X + BORDER_WIDTH + max(arr_x)
    tank_min_y = FIELD_Y + BORDER_WIDTH + max(arr_y)
    touch = contact_with_field_boundaries(tank.body)
    if touch == "x":
        new_x = -tank.body.rectangle.centre.x + max(tank_min_x, min(tank.body.rectangle.centre.x, tank_max_x))
        Tank.move_tank(tank, Rectangle.create_point(new_x, 0))
        tank.speed.x = 0
    elif touch == "y":
        new_y = -tank.body.rectangle.centre.y + max(tank_min_y, min(tank.body.rectangle.centre.y, tank_max_y))
        Tank.move_tank(tank, Rectangle.create_point(0, new_y))
        tank.speed.y = 0


def update_physics():
    """
    All the physics of this game
    :return:
    """
    global last_time, tank1
    cur_time = time.time()
    if last_time:
        dt = cur_time - last_time
        dx_tank = tank1.speed.x * dt
        dy_tank = tank1.speed.y * dt
        Tank.move_tank(tank1, Rectangle.create_point(dx_tank, dy_tank))

        process_rotate_tower(mouse_position, tank1)
        bullets_movement(dt)
        accommodation_targets()
        contact_with_target()
        tank_with_field(tank1)

        tanks()
        draw_tank(tank1)
        for i in range(len(arr_tanks)):
            draw_tank(arr_tanks[i])
# Почему-то рисует только последний танк
    last_time = cur_time
    # update physics as frequent as possible
    root.after(16, update_physics)


root = tk.Tk()

pi = math.pi

SCREEN_WIDTH = root.winfo_screenwidth() - 66
SCREEN_HEIGHT = root.winfo_screenheight() - 66

TITLE_Y = 20
# Field
FIELD_PADDING = 30
BORDER_WIDTH = 5
FIELD_X = FIELD_PADDING
FIELD_Y = FIELD_PADDING + TITLE_Y
FIELD_WIDTH = SCREEN_WIDTH - FIELD_X - FIELD_PADDING
FIELD_HEIGHT = SCREEN_HEIGHT - FIELD_Y - FIELD_PADDING
# Color
COLOR_BORDER = "#808080"
COLOR_FIELD = "#00FF00"
COLOR_TANK = "red"
COLOR_TOWER_TANK = "#0000FF"
COLOR_GUN = "blue"
COLOR_BULLET = "black"
COLOR_TARGET = "yellow"
COLOR_TARGET_STRIP = "#FFC0CB"
COLOR_TANKS = "blue"
COLOR_TANKS_TOWER = "red"
COLOR_TANKS_GUN = "red"
COLOR_SCORE = "black"
TEXT_COLOR_ON_TOP = "black"
# Tank
TANK_WIDTH = 20
TANK_HEIGHT = 40
TOWER_TANK_SIZE = 16
GUN_HEIGHT = 20
GUN_WIDTH = 6
TARGET_HEIGHT = 20
TARGET_WIDTH = 20
START_ROTATE_TANK = pi / 4
TOWER_TURNING_SPEED = 3 * pi / 180
TANK_ACCELERATION = 10
MAXIMUM_SPEED = 400
# Other tanks
START_SPEED_TANK_X = 0
START_SPEED_TANK_Y = 0
TIME_RESPAWN_TANKS = 1
MAXIMUM_NUMBER_OF_TANKS = 10
START_ROTATE_TANKS = [-pi / 2, -pi / 4, 0, pi / 4, pi / 2, pi]
# Bullet
MAXIMUM_NUMBER_OF_BULLET = 100
TIME_RESPAWN_BULLET = 0.33
BULLET_SPEED = 500
# Target
MAXIMUM_NUMBER_OF_TARGETS = 15
TIME_RESPAWN_TARGETS = 1
ROTATE_TARGETS = 0
# Score
START_VALUE_SCORE = 0
X_SCORE = int(SCREEN_WIDTH * 0.9)
Y_SCORE = int((TITLE_Y + FIELD_PADDING) * 0.5)
FONT_SCORE = "Courier"
FONT_SIZE_SCORE = int((TITLE_Y + FIELD_PADDING) * 0.5)
# Text above
X_TEXT = SCREEN_WIDTH / 2
Y_TEXT = int((TITLE_Y + FIELD_PADDING) * 0.5)
FONT_TEXT = FIELD_PADDING
FONT_SIZE_TEXT = int((TITLE_Y + FIELD_PADDING) * 0.3)

arr_bullet = []
arr_bullet_draw = []
arr_target = []
arr_target_draw = []
arr_tanks = []

root.title("Tanks")
root.resizable(False, False)

canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()

text = canvas.create_text(X_TEXT, Y_TEXT,
                          text="Use the WASD buttons to speed up, slow down and turn the tank, use mouse movement\nto "
                               "rotate the tank tower, use LMB to shoot and score points hitting targets,"
                               " use Esc to exit.",
                          font=(FONT_TEXT, FONT_SIZE_TEXT), fill=TEXT_COLOR_ON_TOP)

border = canvas.create_rectangle(FIELD_X, FIELD_Y,
                                 FIELD_X + FIELD_WIDTH, FIELD_Y + FIELD_HEIGHT,
                                 fill=COLOR_FIELD, outline=COLOR_BORDER, width=2 * BORDER_WIDTH)
score = create_score(START_VALUE_SCORE, COLOR_SCORE, X_SCORE, Y_SCORE, FONT_SCORE, FONT_SIZE_SCORE)
tank1 = Tank.create_tank(FIELD_X + FIELD_WIDTH / 2, FIELD_Y + FIELD_HEIGHT / 2, TANK_HEIGHT, TANK_WIDTH, COLOR_TANK,
                         TOWER_TANK_SIZE, TOWER_TANK_SIZE, COLOR_TOWER_TANK, GUN_HEIGHT, GUN_WIDTH, COLOR_GUN,
                         START_SPEED_TANK_X, START_SPEED_TANK_Y, START_ROTATE_TANK)
draw_tank(tank1)
mouse_position = Rectangle.create_point(FIELD_X + FIELD_WIDTH / 2, FIELD_Y + FIELD_HEIGHT / 2)
last_time = time.time()
time_for_target = time.time()
time_for_bullet = time.time()
time_for_tanks = time.time()

root.bind("<Key>", process_key)
root.bind("<Button-1>", process_shot)
root.bind("<Motion>", mouse_position_memorization)

Test_rectangle.tests()

update_physics()
root.mainloop()

