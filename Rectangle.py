import math


class Point:
    x = None
    y = None


class Rectangle:
    centre: Point = None
    sizes: Point = None
    rotate = None
    color = None


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
    if rectangle.rotate > math.pi:
        rectangle.rotate -= 2 * math.pi
    if rectangle.rotate <= -math.pi:
        rectangle.rotate += 2 * math.pi
    rectangle.rotate += angle_change


def move_rectangle(rectangle: Rectangle, dr: Point) -> None:
    rectangle.centre.x += dr.x
    rectangle.centre.y += dr.y


def points_rectangle(rectangle: Rectangle):
    """
    Sets 4 vertices of a rectangle
    :param rectangle:
    :return:
    """
    lenght = math.hypot(rectangle.sizes.x, rectangle.sizes.y)
    start_rotate = math.atan(rectangle.sizes.x / rectangle.sizes.y)
    point_1x, point_1y = lenght * math.cos(rectangle.rotate + start_rotate), lenght * math.sin(
        rectangle.rotate + start_rotate)
    point_2x, point_2y = lenght * math.cos(rectangle.rotate - start_rotate), lenght * math.sin(
        rectangle.rotate - start_rotate)
    point_3x, point_3y = lenght * math.cos(
        rectangle.rotate + start_rotate + math.pi), lenght * math.sin(rectangle.rotate + start_rotate + math.pi)
    point_4x, point_4y = lenght * math.cos(
        rectangle.rotate - start_rotate + math.pi), lenght * math.sin(rectangle.rotate - start_rotate + math.pi)
    arr_x = [point_1x, point_2x, point_3x, point_4x]
    arr_y = [point_1y, point_2y, point_3y, point_4y]
    return arr_x, arr_y


def intersection(rectangle1: Rectangle, rectangle2: Rectangle) -> bool:
    """
    Is the center of the second rectangle inside the first rectangle
    :param rectangle1:
    :param rectangle2:
    :return:
    """
    return in_rectangle(rectangle1, create_point(rectangle2.centre.x, rectangle2.centre.y))


def in_rectangle(rectangle: Rectangle, point: Point) -> bool:
    """
    finds out if the point is inside the rectangle
    :param rectangle:
    :param point:
    :return:
    """
    arr_x = [rectangle.centre.x - rectangle.sizes.x, rectangle.centre.x + rectangle.sizes.x]
    arr_y = [rectangle.centre.y - rectangle.sizes.y, rectangle.centre.y + rectangle.sizes.y]
    if arr_x[0] < point.x < arr_x[1] and arr_y[0] < point.y < arr_y[1]:
        return True
    return False

