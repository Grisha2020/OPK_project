import math
import Rectangle
import Tank


class Bullet:
    rectangle: Rectangle.Rectangle = None
    speed: Rectangle.Point = None


class Target:
    rectangle: Rectangle = None


def create_bullet(tank: Tank.Tank, speed: int, color: str) -> Bullet:
    """
    Creates a bullet at the end of a tank gun
    :param tank:
    :param speed:
    :param color:
    :return:
    """
    bullet = Bullet()
    x_centre, y_centre = tank.gun.rectangle.centre.x + math.hypot(tank.gun.rectangle.sizes.x,
                                                                  tank.gun.rectangle.sizes.y) * math.cos(
        tank.gun.rectangle.rotate - math.pi / 2), tank.gun.rectangle.centre.y + math.hypot(tank.gun.rectangle.sizes.x,
                                                                                           tank.gun.rectangle.sizes.y) * math.sin(
        tank.gun.rectangle.rotate - math.pi / 2)
    bullet.rectangle = Rectangle.create_rectangle(x_centre, y_centre, tank.gun.rectangle.sizes.y,
                                                  tank.gun.rectangle.sizes.y, tank.gun.rectangle.rotate, color)
    bullet.speed = Rectangle.create_point(speed * math.cos(bullet.rectangle.rotate - math.pi / 2),
                                          speed * math.sin(bullet.rectangle.rotate - math.pi / 2))
    return bullet


def move_bullet(bullet: Bullet, dr: Rectangle.Point) -> None:
    Rectangle.move_rectangle(bullet.rectangle, dr)


def create_target(x_centre: int, y_centre: int, height: int, width: int, start_rotate, color) -> Target:
    target = Target()
    target.rectangle = Rectangle.create_rectangle(x_centre, y_centre, height, width, start_rotate, color)
    return target

