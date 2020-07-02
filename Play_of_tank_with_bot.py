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


class HealthBar:
    number_of_shots: int = None
    damage: int = None
    start: Rectangle.Point = None
    length: int = None
    color: str = None
    width: int = None
    draw_bar = None


def draw_rectangle(rectangle: Rectangle.Rectangle):
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
    """
    Draws all three parts of the tank (body, turret and gun)
    :param tank:
    :return:
    """
    # if len(tank.polygons) != 0:
    #     for i in range(len(tank.polygons)):
    #         canvas.delete(tank.polygons[i])
    #     tank.polygons = []
    del_tank_polygons(tank)
    tank.polygons.append(draw_rectangle(tank.body.rectangle))
    tank.polygons.append(draw_rectangle(tank.tower.rectangle))
    tank.polygons.append(draw_rectangle(tank.gun.rectangle))


def del_tank_polygons(tank: Tank):
    if len(tank.polygons) != 0:
        for i in range(len(tank.polygons)):
            canvas.delete(tank.polygons[i])
        tank.polygons = []


def draw_bullet(bullet: Bullet_and_target.Bullet):
    return draw_rectangle(bullet.rectangle)


def create_score(value: int, color: str, centre_x: int, centre_y: int, font: str, font_size: int) -> Score:
    score_1 = Score()
    score_1.value = value
    score_1.draw_score = canvas.create_text(centre_x, centre_y, text=value, font=(font, font_size), fill=color)
    return score_1


def change_score(score_1: Score, increase: int) -> None:
    score_1.value += increase
    canvas.itemconfig(score_1.draw_score, text=score_1.value)


def create_health_bar(number_of_shots: int, health_x: int, health_y: int, length: int, color: str,
                      width: int) -> HealthBar:
    health_return = HealthBar()
    health_return.number_of_shots = number_of_shots
    health_return.damage = 0
    health_return.start = Rectangle.create_point(health_x, health_y)
    health_return.length = length
    health_return.color = color
    health_return.width = width
    health_return.draw_bar = canvas.create_line(health_return.start.x, health_return.start.y,
                                                health_return.start.x + health_return.length, health_return.start.y,
                                                fill=health_return.color, width=health_return.width)
    return health_return


def change_health(health_copy: HealthBar) -> None:
    canvas.delete(health_copy.draw_bar)
    health_copy.draw_bar = canvas.create_line(health_copy.start.x, health_copy.start.y,
                                              health_copy.start.x + health_copy.length * (
                                                      health_copy.number_of_shots - health_copy.damage) /
                                              health_copy.number_of_shots,
                                              health_copy.start.y, fill=health_copy.color, width=health_copy.width)


def process_shot(event) -> None:
    shots(tank1, TIME_RESPAWN_BULLET)


def shots(tank: Tank.Tank, time_respawn) -> None:
    global arr_bullet
    if tank.time_shot + time_respawn < time.time():
        if len(arr_bullet) <= MAXIMUM_NUMBER_OF_BULLET:
            bullet = Bullet_and_target.create_bullet(tank, BULLET_SPEED, COLOR_BULLET)
            arr_bullet.append(bullet)
            arr_bullet_draw.append(draw_bullet(bullet))
            tank.time_shot = time.time()


def process_key(event) -> None:
    dspeed = 0
    # event.char - regular symbols
    # event.keysym - special keys
    if event.keysym == "Up" or event.char == "w" or event.char == "ц":
        dspeed += TANK_ACCELERATION
    elif event.keysym == "Down" or event.char == "s" or event.char == "ы":
        dspeed -= TANK_ACCELERATION
    elif event.keysym == "Left" or event.char == "a" or event.char == "ф":
        Tank.rotate_tank(tank1, -TANK_TURNING_SPEED)
    elif event.keysym == "Right" or event.char == "d" or event.char == "в":
        Tank.rotate_tank(tank1, TANK_TURNING_SPEED)
    elif event.keysym == "Escape":
        root.quit()
        return
    Tank.speed_change(dspeed, tank1, MAXIMUM_SPEED)


def mouse_position_memorization(event) -> None:
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
    if abs(angle - tank.tower.rectangle.rotate) >= TOWER_TURNING_SPEED:
        if angle > 0:
            if angle - pi <= tank.tower.rectangle.rotate <= angle:
                Tank.rotate_tower_gun(tank, TOWER_TURNING_SPEED)
            elif -pi <= tank.tower.rectangle.rotate <= angle - pi or angle < tank.tower.rectangle.rotate < pi:
                Tank.rotate_tower_gun(tank, -TOWER_TURNING_SPEED)
        else:
            if angle <= tank.tower.rectangle.rotate <= angle + pi:
                Tank.rotate_tower_gun(tank, -TOWER_TURNING_SPEED)
            elif -pi <= tank.tower.rectangle.rotate <= angle or angle + pi < tank.tower.rectangle.rotate < pi:
                Tank.rotate_tower_gun(tank, TOWER_TURNING_SPEED)
    else:
        if angle > 0:
            if angle - pi <= tank.tower.rectangle.rotate <= angle:
                Tank.rotate_tower_gun(tank, pi / 360)
            elif -pi <= tank.tower.rectangle.rotate <= angle - pi or angle < tank.tower.rectangle.rotate < pi:
                Tank.rotate_tower_gun(tank, -pi / 360)
        else:
            if angle <= tank.tower.rectangle.rotate <= angle + pi:
                Tank.rotate_tower_gun(tank, -pi / 360)
            elif -pi <= tank.tower.rectangle.rotate <= angle or angle + pi < tank.tower.rectangle.rotate < pi:
                Tank.rotate_tower_gun(tank, pi / 360)


def tanks():
    global arr_tanks, time_for_tanks
    if time_for_tanks + TIME_RESPAWN_TANKS < last_time:
        if len(arr_tanks) < MAXIMUM_NUMBER_OF_TANKS:
            flag_of_tanks = False
            new_point = Rectangle.create_point(0, 0)
            counter = 0
            while flag_of_tanks is False:
                if counter >= 5:
                    return
                new_point.x, new_point.y = \
                    random.randrange(FIELD_X + BORDER_WIDTH + int(math.hypot(TANK_HEIGHT, TANK_WIDTH) + 1), FIELD_X +
                                     FIELD_WIDTH - BORDER_WIDTH - int(math.hypot(TANK_HEIGHT, TANK_WIDTH) + 1)), \
                    random.randrange(FIELD_Y + BORDER_WIDTH + int(math.hypot(TANK_HEIGHT, TANK_WIDTH) + 1), FIELD_Y +
                                     FIELD_HEIGHT - BORDER_WIDTH - int(math.hypot(TANK_HEIGHT, TANK_WIDTH) + 1))
                flag_1 = False
                for i in range(len(arr_tanks)):
                    if Rectangle.in_rectangle(arr_tanks[i].body.rectangle, new_point,
                                              int(math.hypot(TANK_HEIGHT, TANK_WIDTH) + 1)) is True:
                        flag_1 = True
                        break
                if flag_1 is True:
                    counter += 1
                    continue
                if Rectangle.in_rectangle(tank1.body.rectangle, new_point,
                                          int(math.hypot(TANK_HEIGHT, TANK_WIDTH) + 1)) is True:
                    counter += 1
                    continue
                flag_of_tanks = True
            arr_tanks.append(
                Tank.create_tank(new_point.x, new_point.y, TANK_HEIGHT, TANK_WIDTH, COLOR_TANKS, TOWER_TANK_SIZE,
                                 TOWER_TANK_SIZE, COLOR_TANKS_TOWER, GUN_HEIGHT, GUN_WIDTH, COLOR_TANKS_GUN,
                                 START_SPEED_TANK_X, START_SPEED_TANK_Y,
                                 START_ROTATE_TANKS[random.randint(0, len(START_ROTATE_TANKS) - 1)], time.time()))
            time_for_tanks = last_time


def move_other_tanks(dt) -> None:  # Нужно, чтобы танки двигались не рывками, а плавно(добавить запоминание последнего
    # движения)
    global arr_tanks
    for i in range(len(arr_tanks)):
        direction = random.choice(['w', 'a', 's', 'd'])
        factor = random.randint(1, 3)
        dspeed = 0
        if direction == 'w':
            dspeed += factor * TANK_ACCELERATION
        elif direction == 's':
            dspeed -= factor * TANK_ACCELERATION
        elif direction == 'a':
            Tank.rotate_tank(arr_tanks[i], -(factor * TANK_TURNING_SPEED))
        elif direction == 'd':
            Tank.rotate_tank(arr_tanks[i], factor * TANK_TURNING_SPEED)
        Tank.speed_change(dspeed, arr_tanks[i], MAXIMUM_SPEED)
        dx_tank = arr_tanks[i].speed.x * dt
        dy_tank = arr_tanks[i].speed.y * dt
        Tank.move_tank(arr_tanks[i], Rectangle.create_point(dx_tank, dy_tank))
        tank_with_field(arr_tanks[i])
        process_rotate_tower(tank1.body.rectangle.centre, arr_tanks[i])
        shots(arr_tanks[i], TIME_RESPAWN_BULLET_OTHER_TANK)


def contact_bullet_with_other_tanks() -> None:
    """
    There was contact between bullets and targets, also between the tank and targets
    :return:
    """
    global arr_bullet, arr_bullet_draw, arr_tanks
    if len(arr_tanks) > 0:
        arr_del_bul_1 = []
        arr_del_tan = []
        for i in range(len(arr_tanks)):
            for j in range(len(arr_bullet)):
                if Rectangle.intersection(arr_tanks[i].body.rectangle, arr_bullet[j].rectangle) is True:
                    arr_del_bul_1.append(j)
                    arr_del_tan.append(i)
                    break
        for i in range(len(arr_del_tan)):
            try:
                canvas.delete(arr_bullet_draw[arr_del_bul_1[len(arr_del_tan) - i - 1]])
                del arr_bullet_draw[arr_del_bul_1[len(arr_del_tan) - i - 1]]
                del arr_bullet[arr_del_bul_1[len(arr_del_tan) - i - 1]]
                del_tank_polygons(arr_tanks[arr_del_tan[len(arr_del_tan) - i - 1]])
                del arr_tanks[arr_del_tan[len(arr_del_tan) - i - 1]]
                change_score(score, 1)
            except IndexError:
                continue


def contact_bullet_with_main_tank():
    global arr_bullet, arr_bullet_draw, health
    if len(arr_bullet) > 0:
        arr_del_bul = []
        for i in range(len(arr_bullet)):
            if Rectangle.intersection(tank1.body.rectangle, arr_bullet[i].rectangle) is True:
                arr_del_bul.append(i)
                break
        for i in range(len(arr_del_bul)):
            canvas.delete(arr_bullet_draw[arr_del_bul[len(arr_del_bul) - i - 1]])
            del arr_bullet_draw[arr_del_bul[len(arr_del_bul) - i - 1]]
            del arr_bullet[arr_del_bul[len(arr_del_bul) - i - 1]]
            health.damage += 1
            change_health(health)


def contact_tank_with_tanks():
    global arr_tanks  # Сделать соприкосновение бота с ботом
    # if len(arr_tanks) > 0:
    #     arr_del_tan = []
    #     for i in range(len(arr_tanks)):
    #         for j in range(0, len(arr_tanks) - i, -1):
    #             if Rectangle.intersection(arr_tanks[i].body.rectangle, arr_tanks[j].body.rectangle) is True:
    #                 arr_del_tan.append(i)
    #                 arr_del_tan.append(len(arr_tanks) - j)
    #                 break
    #     for i in range(len(arr_del_tan)):
    #         try:
    #             del_tank_polygons(arr_tanks[arr_del_tan[len(arr_del_tan) - i - 1]])
    #             del arr_tanks[arr_del_tan[len(arr_del_tan) - i - 1]]
    #             change_score(score, 1)
    #         except IndexError:
    #             continue
    if len(arr_tanks) > 0:
        arr_del_tan = []
        for i in range(len(arr_tanks)):
            if Rectangle.intersection(arr_tanks[i].body.rectangle, tank1.body.rectangle) is True:
                arr_del_tan.append(i)
                break
        for i in range(len(arr_del_tan)):
            try:
                del_tank_polygons(arr_tanks[arr_del_tan[len(arr_del_tan) - i - 1]])
                del arr_tanks[arr_del_tan[len(arr_del_tan) - i - 1]]
                change_score(score, 1)
                health.damage += 1
                change_health(health)
            except IndexError:
                continue


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


def bullets_movement(dt) -> None:  # Почему-то пропадают те снаряды, которые не должны пропадать
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
    if health.damage == health.number_of_shots:
        root.quit()
        return  # Надо вместо закрытия сделать всплывающее окно где будет спрашиваться у пользователя хочет он
        # перезапустить или нет
    cur_time = time.time()
    if last_time:
        dt = cur_time - last_time
        dx_tank = tank1.speed.x * dt
        dy_tank = tank1.speed.y * dt
        Tank.move_tank(tank1, Rectangle.create_point(dx_tank, dy_tank))

        process_rotate_tower(mouse_position, tank1)
        contact_bullet_with_main_tank()
        bullets_movement(dt)
        tanks()
        tank_with_field(tank1)
        move_other_tanks(dt)
        contact_bullet_with_other_tanks()
        contact_tank_with_tanks()
        draw_tank(tank1)

        draw_tank(tank1)
        for i in range(len(arr_tanks)):
            draw_tank(arr_tanks[i])

    last_time = cur_time
    # update physics as frequent as possible
    root.after(16, update_physics)


root = tk.Tk()

pi = math.pi

SCREEN_WIDTH = root.winfo_screenwidth() - 66
SCREEN_HEIGHT = root.winfo_screenheight() - 66

TITLE_Y = 20  # 20
# Field
FIELD_PADDING = 30  # 30
BORDER_WIDTH = 5  # 5

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
COLOR_SCORE = "blue"
TEXT_COLOR_ON_TOP = "black"
COLOR_TANKS = "blue"
COLOR_TANKS_TOWER = "red"
COLOR_TANKS_GUN = "red"
COLOR_HEALTH_BAR = "red"  # yellow
# Tank
TANK_WIDTH = 20  # 20
TANK_HEIGHT = 40  # 40
TOWER_TANK_SIZE = 16  # 16
GUN_HEIGHT = 20  # 20
GUN_WIDTH = 6  # 6
START_ROTATE_TANK = 0  # 0
TANK_TURNING_SPEED = 5 * pi / 180  # 5 * pi / 180
TOWER_TURNING_SPEED = 3 * pi / 180  # 3 * pi / 180
TANK_ACCELERATION = 10  # 10
MAXIMUM_SPEED = 400  # 400
NUMBER_OF_SHOTS_TO_DESTROY_THE_MAIN_TANK = 10  # 10
HEALTH_X = int(SCREEN_WIDTH * 0.9)
HEALTH_Y = int((TITLE_Y + FIELD_PADDING) * 1.5)
LENGTH_HEALTH_BAR = 150  # 150
WIDTH_HEALTH_BAR = 15  # 15
# Other tanks
START_SPEED_TANK_X = 0  # 0
START_SPEED_TANK_Y = 0  # 0
TIME_RESPAWN_TANKS = 3  # 3
MAXIMUM_NUMBER_OF_TANKS = 3  # 3
START_ROTATE_TANKS = [-pi / 2, -pi / 4, 0, pi / 4, pi / 2, pi]
TIME_RESPAWN_BULLET_OTHER_TANK = 2  # 2
# Bullet
MAXIMUM_NUMBER_OF_BULLET = 100  # 100
TIME_RESPAWN_BULLET = 0.33  # 0.33
BULLET_SPEED = 500  # 500
# Score
START_VALUE_SCORE = 0  # 0
X_SCORE = int(SCREEN_WIDTH * 0.9)
Y_SCORE = int((TITLE_Y + FIELD_PADDING) * 0.5)
FONT_SCORE = "Courier"
FONT_SIZE_SCORE = int((TITLE_Y + FIELD_PADDING) * 0.45)
# Text above
X_TEXT = SCREEN_WIDTH / 2
Y_TEXT = int((TITLE_Y + FIELD_PADDING) * 0.5)
FONT_TEXT = FIELD_PADDING
FONT_SIZE_TEXT = int((TITLE_Y + FIELD_PADDING) * 0.2)

arr_bullet = []
arr_bullet_draw = []
arr_tanks = []

root.title("Tank")
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
                         TOWER_TANK_SIZE, TOWER_TANK_SIZE, COLOR_TOWER_TANK, GUN_HEIGHT, GUN_WIDTH, COLOR_GUN, 0, 0,
                         START_ROTATE_TANK, time.time())
draw_tank(tank1)

health = create_health_bar(NUMBER_OF_SHOTS_TO_DESTROY_THE_MAIN_TANK, HEALTH_X, HEALTH_Y, LENGTH_HEALTH_BAR,
                           COLOR_HEALTH_BAR, WIDTH_HEALTH_BAR)

mouse_position = Rectangle.create_point(FIELD_X + FIELD_WIDTH / 2, FIELD_Y + FIELD_HEIGHT / 2)
last_time = time.time()
time_for_tanks = time.time()

root.bind("<Key>", process_key)
root.bind("<Button-1>", process_shot)
root.bind("<Motion>", mouse_position_memorization)
# Button-1 space
Test_rectangle.tests()

update_physics()
root.mainloop()

