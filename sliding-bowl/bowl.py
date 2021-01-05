import math
from solid import *
from solid.utils import *

from moveable_point import *

def cos(a):
    return math.cos(math.radians(a))

def tan(a):
    return math.tan(math.radians(a))

def atan(a):
    return math.degrees(math.atan(a))

def gradient():
    x = 81.0
    y = 41.0
    thick = 1.8
    thin = 0.9
    support_count = 5

    angle = atan(x / (support_count * y))

    short_side_diff_half = y * tan(22.5) * cos(angle)

    p = MoveablePoint()
    panel = left(x / 2)(linear_extrude(thin)(polygon([
        p.right(short_side_diff_half).val(),
        [0, y],
        [x, y],
        p.set(x = x, y = 0).left(short_side_diff_half).val(),
    ])))
    panel = rotate(angle, RIGHT_VEC)(panel)

    support = linear_extrude(thick)(polygon([
        p.reset().val(),
        p.up(y).val(),
        p.right(x / support_count).val(),
    ]))
    support = right(thick / 2)(rotate(90, BACK_VEC)(support))

    short_side = x - (2 * short_side_diff_half)
    support_gap = (short_side - (thick * 2)) / (support_count - 1)

    model = panel
    for i in range(support_count):
        model += right((i * support_gap) - (short_side / 2) + thick)(support)

    model = forward((x / 0.828) - (y * cos(angle)))(model)

    return model

if __name__ == '__main__':
    model = forward(30)(rotate(90, RIGHT_VEC)(scale(0.1)(import_stl('person.stl'))))

    for i in range(0, 360, 45):
        model += rotate(i, UP_VEC)(gradient())
    
    scad_render_to_file(model, '_%s.scad'% __file__.split('/')[-1][:-3])


