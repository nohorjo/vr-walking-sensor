import math
import os
from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

def cos(a):
    return math.cos(math.radians(a))

def tan(a):
    return math.tan(math.radians(a))

plank_count = 0.0
plank_t = 2.1

space_size = 220.0
pace = 40.0
angle = 20

padding = pace * cos(angle)
walk_space = space_size - (padding * 2)
side_length = walk_space * 0.4142
small_side = side_length * 0.70711

def plank(length = 100, count_x = 1, count_z = 1):
    global plank_count
    x = 9.0

    count_y = length / 100
    plank_count += ceil(count_x * count_y * count_z)

    base = cube([x, length, plank_t])
    model = base

    for i in range(count_x - 1):
        model += right((x + 0.2) * (i + 1))(base)
    base = model
    for i in range(ceil(count_y) - 1):
        model += forward((length + 0.2) * (i + 1))(base)
    base = model
    for i in range(count_z - 1):
        model += up((plank_t + 0.2) * (i + 1))(base)
    return model

def base():
    p = MoveablePoint()
    model = linear_extrude(plank_t)(polygon([
        p.forward(side_length).rotate(45).val() for i in range(8)
    ])) * left(small_side)(plank(count_x = 16, length = walk_space))

    return translate([-side_length / 2, -walk_space / 2])(model)

def gradient():
    p = MoveablePoint()
    y = 15.5
    model = linear_extrude(plank_t)(polygon([
        p.val(),
        p.up(side_length).val(),
        p.up(y).right(pace).val(),
        p.down(side_length + (y * 2)).val(),
    ]))

    model *= back(y)(plank(count_x = 5))

    def support():
        return rotate(90, DOWN_VEC)(
            rotate(90, BACK_VEC)(plank(length = padding, count_x = 2))
        )

    flat = model
    model = rotate(angle, BACK_VEC)(model)

    gap = 15
    supports = support()
    for i in range(gap, round(side_length), gap):
        supports += forward(i)(support())
    supports *= hull()(model + flat)
    supports = back((y / 2) - gap)(supports)

    model += supports

    return translate([walk_space / 2, -side_length / 2])(model)

if __name__ == '__main__':
    model = translate([0, 30, plank_t])(rotate(90, RIGHT_VEC)(scale(0.1)(import_stl('person.stl'))))
    #  model += base()

    angled_parts = gradient()
    for i in range(45, 360, 45):
        angled_parts += rotate(i, UP_VEC)(gradient())

    model += angled_parts
    
    scad_render_to_file(model, '_%s.scad'% __file__.split('/')[-1][:-3])

    if not os.environ.get('FROM_VIM'):
        print(plank_count)

