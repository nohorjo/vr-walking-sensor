from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

if __name__ == '__main__':
    size = 12.0
    offset = 3.5

    hole = cylinder(d = screw_d, h = size)

    model = cube(size)
    model -= translate([offset, offset])(hole)
    model -= translate([0, size - offset, offset])(rotate(90, FORWARD_VEC)(hole))

    scad_render_to_file(model, '_%s.scad'% __file__.split('/')[-1][:-3])

