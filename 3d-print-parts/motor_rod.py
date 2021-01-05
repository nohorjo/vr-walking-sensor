from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

if __name__ == '__main__':
    x = 25.0
    y = 7.0
    z = 5.0

    model = cube([x, y, z])

    y2 = 3.2

    model -= translate([2, (y - y2) / 2])(cube([5, y2, 10]))
    model -= translate([x - 3, 0, z / 2])(rotate(90, LEFT_VEC)(cylinder(d = cable_d, h = 10)))

    scad_render_to_file(model, '_%s.scad'% __file__.split('/')[-1][:-3])

