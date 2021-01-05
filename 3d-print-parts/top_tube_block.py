from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

if __name__ == '__main__':
    x = 13.0
    y = 8.0

    p = MoveablePoint()

    model = cube([x, y, 3])
    model += cube([5.5, y, 7])
    model -= translate([(x / 2) + 2, y / 2])(cylinder(d = tube_d, h = 10))

    scad_render_to_file(model, '_%s.scad'% __file__.split('/')[-1][:-3])

