from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

if __name__ == '__main__':
    y = 15.0

    model = cube([2, y, 15])
    model += cube([y, y, 3])
    model -= translate([(y + 3) / 2, y / 2])(cylinder(d = screw_d, h = 10))

    scad_render_to_file(model, '_%s.scad'% __file__.split('/')[-1][:-3])

