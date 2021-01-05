from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

if __name__ == '__main__':
    x = 3.9
    y = 10.0

    model = translate([-x / 2, -y / 2])(cube([x, y, 3.5]))
    model -= up(3.25)(cube([x, y - 3, 2], True))
    model -= up(1)(cylinder(d = cable_d, h = 10))

    scad_render_to_file(model, '_%s.scad'% __file__.split('/')[-1][:-3])

