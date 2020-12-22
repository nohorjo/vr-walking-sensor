from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

def strap():
    h = 90.0
    model = hull()(cylinder(d = 80) + up(h)(cylinder(d = 120)))
    model *= translate([-h, 10])(cube(h * 2))

    sf = 0.95
    model -= super_hole(translate([0, -1, -1])(scale([sf, sf, 1.1])(model)), 'leg_hole')

    model = minkowski()(sphere(r = 1), model)

    holes = cube([200, 5, 25])
    holes += up(h - 40)(holes)
    holes = translate([-100, 15, 10])(holes)

    model -= super_hole(holes, 'strap_hole')

    return model

def component_block(is_right):
    battery_dims = [65.0, 10.0, 67.0]
    t = 2.5
    x = battery_dims[0] + t
    y = 35.0
    battery_block = cube([x, y, battery_dims[2] + t]) - translate([t / 2, y - battery_dims[1] + 0.01, t / 2])(super_hole(cube(battery_dims), 'battery_block'))
    battery_block += cube([85, 20, 30])
    battery_block = rotate(10, LEFT_VEC)(battery_block)

    sensor_block = forward(25)(cube([20, 10, 12])) + forward(10)(cube([20, 25, 6]))
    if is_right:
        sensor_block = translate([20, 35])(rotate(180, UP_VEC)(sensor_block))

    battery_block += translate([0, 22, 61])(sensor_block)

    model = translate([-x / 2, 28, 20])(battery_block)

    model -= strap()

    return model

if __name__ == '__main__':
    model = strap()
    scad_render_to_file(model, '_%s.scad'% __file__[:-3])
