from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

if __name__ == '__main__':
    model = cylinder(d = 50, h = 2)
    model += cylinder(d1 = 25, d2 = 11, h = 20)
    model -= cylinder(d = mirror_stick_d, h = 100)

    scad_render_to_file(model, '_%s.scad'% __file__.split('/')[-1][:-3])

