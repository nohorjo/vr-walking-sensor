from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

if __name__ == '__main__':
    model = cube([25, 25, 2])
    model += translate([8, 8])(
        cube([12, 3, 8])
        + translate([6, 0, 10])(rotate(90, LEFT_VEC)(
            cylinder(d = 13, h = 3)
            - cylinder(d = screw_d, h = 10)
        ))
    )
    scad_render_to_file(model, '_%s.scad'% __file__.split('/')[-1][:-3])

