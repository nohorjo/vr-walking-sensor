from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

t = 2.5

def platform_with_holes(x, y):
    model = cube([x, y, t])
    
    hole_d = 3.5
    hole_offset = 1.7
    for a in [hole_offset + (hole_d / 2), y - hole_offset - (hole_d / 2)]:
        model -= translate([4, a])(cylinder(d = hole_d, h = t))

    return model

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

if __name__ == '__main__':
    model = strap()

    scad_render_to_file(model, '_%s.scad'% __file__.split('/')[-1][:-3])
