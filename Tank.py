import math
import Rectangle


class Body:
    rectangle: Rectangle.Rectangle = None


class Tower:
    rectangle: Rectangle.Rectangle = None


class Gun:
    rectangle: Rectangle.Rectangle = None


class Tank:
    body: Body = None
    tower: Tower = None
    gun: Gun = None
    speed: Rectangle.Point = None
    polygons = []


def create_tank(centre_x: int, centre_y: int, height_body: int, width_body: int, color_body: str, height_tower: int,
                width_tower: int, color_tower: str, height_gun: int, width_gun: int, color_gun: str, speed_x: int,
                speed_y: int) -> Tank:
    tank = Tank()
    tank.body = Body()
    tank.body.rectangle = Rectangle.create_rectangle(centre_x, centre_y, height_body, width_body, 0, color_body)
    tank.tower = Tower()
    tank.tower.rectangle = Rectangle.create_rectangle(centre_x, centre_y, height_tower, width_tower, 0, color_tower)
    tank.gun = Gun()
    tank.gun.rectangle = Rectangle.create_rectangle(centre_x, centre_y - height_tower - height_gun, height_gun,
                                                    width_gun, 0, color_gun)
    tank.speed = Rectangle.create_point(speed_x, speed_y)
    return tank


def move_tank(tank: Tank, dr: Rectangle.Point) -> None:
    Rectangle.move_rectangle(tank.body.rectangle, dr)
    Rectangle.move_rectangle(tank.tower.rectangle, dr)
    Rectangle.move_rectangle(tank.gun.rectangle, dr)


def rotate_tank(tank: Tank, angle_change) -> None:
    """
    Turns all parts of the tank
    :param tank:
    :param angle_change:
    :return:
    """
    Rectangle.rotate_rectangle(tank.body.rectangle, angle_change)
    Rectangle.rotate_rectangle(tank.tower.rectangle, angle_change)
    Rectangle.rotate_rectangle(tank.gun.rectangle, angle_change)
    tank.gun.rectangle.centre.x, tank.gun.rectangle.centre.y = \
        tank.tower.rectangle.centre.x + (tank.tower.rectangle.sizes.y + tank.gun.rectangle.sizes.x) * \
        math.cos(tank.tower.rectangle.rotate - math.pi / 2), \
        tank.tower.rectangle.centre.y + (tank.tower.rectangle.sizes.y + tank.gun.rectangle.sizes.x) * \
        math.sin(tank.tower.rectangle.rotate - math.pi / 2)


def rotate_tower_gun(tank: Tank, angle_change) -> None:
    """
    Turns only the tower and gun of the tank
    :param tank:
    :param angle_change:
    :return:
    """
    Rectangle.rotate_rectangle(tank.tower.rectangle, angle_change)
    Rectangle.rotate_rectangle(tank.gun.rectangle, angle_change)
    tank.gun.rectangle.centre.x, tank.gun.rectangle.centre.y = \
        tank.tower.rectangle.centre.x + (tank.tower.rectangle.sizes.y + tank.gun.rectangle.sizes.x) * \
        math.cos(tank.tower.rectangle.rotate - math.pi / 2), \
        tank.tower.rectangle.centre.y + (tank.tower.rectangle.sizes.y + tank.gun.rectangle.sizes.x) * \
        math.sin(tank.tower.rectangle.rotate - math.pi / 2)


def speed_change(dspeed: int, tank: Tank) -> None:
    """
    Changes the speed of all parts of the tank
    :param dspeed:
    :param tank:
    :return:
    """
    speed = math.hypot(abs(tank.speed.x), abs(tank.speed.y))
    tank.speed.x = (speed + dspeed) * math.cos(
        tank.body.rectangle.rotate - math.pi / 2)
    tank.speed.y = (speed + dspeed) * math.sin(
        tank.body.rectangle.rotate - math.pi / 2)
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

