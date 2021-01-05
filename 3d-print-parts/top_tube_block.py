from solid import *
from solid.utils import *

from constants import *

if __name__ == '__main__':
    model = cube([25, 2, 10])
    model += cube([10, 10, 4])
    model -= translate([5, 5])(
        cylinder(d = tube_d, h = 10)
        + left(cable_d / 2)(cube([cable_d + 0.1, 10, 10]))
    )

    scad_render_to_file(model, '_%s.scad'% __file__.split('/')[-1][:-3])

