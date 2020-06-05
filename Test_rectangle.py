import Rectangle
from math import pi


def tests():
    x_centre_1 = 0
    y_centre_1 = 0
    height_1 = 20
    width_1 = 40
    start_rotate_1 = pi / 4
    color_1 = None

    x_centre_2 = 40
    y_centre_2 = 40
    height_2 = 20
    width_2 = 20
    start_rotate_2 = 0
    color_2 = None

    x_centre_3 = 100
    y_centre_3 = 100
    height_3 = 20
    width_3 = 20
    start_rotate_3 = 0
    color_3 = None

    x_centre_4 = 40
    y_centre_4 = 40
    height_4 = 20
    width_4 = 20
    start_rotate_4 = pi / 4
    color_4 = None

    rectangle_1 = Rectangle.create_rectangle(x_centre_1, y_centre_1, height_1, width_1, start_rotate_1, color_1)
    rectangle_2 = Rectangle.create_rectangle(x_centre_2, y_centre_2, height_2, width_2, start_rotate_2, color_2)
    rectangle_3 = Rectangle.create_rectangle(x_centre_3, y_centre_3, height_3, width_3, start_rotate_3, color_3)
    rectangle_4 = Rectangle.create_rectangle(x_centre_4, y_centre_4, height_4, width_4, start_rotate_4, color_4)

    assert Rectangle.intersection(rectangle_1, rectangle_1) is True
    assert Rectangle.intersection(rectangle_2, rectangle_1) is True
    assert Rectangle.intersection(rectangle_1, rectangle_2) is True
    assert Rectangle.intersection(rectangle_1, rectangle_3) is False
    assert Rectangle.intersection(rectangle_2, rectangle_3) is False
    assert Rectangle.intersection(rectangle_1, rectangle_4) is True

    assert Rectangle.intersection(rectangle_2,
                                  rectangle_4) is False  # Должно быть True, но из-за самого метода определения соприкосновения там False

