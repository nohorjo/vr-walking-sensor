from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

if __name__ == '__main__':
    model = cylinder(d = mirror_stick_d + 4, h = 12)
    model += right(4)(
        cube([3, 15, 12])
        + translate([0, 15, 6])(rotate(90, FORWARD_VEC)(cylinder(d = 13, h = 3)))
    )
    model -= cylinder(d = mirror_stick_d, h = 12)
    model -= up(6)(rotate(90, RIGHT_VEC)(cylinder(d = screw_d, h = 10)))
    model -= translate([0, 15, 6])(rotate(90, FORWARD_VEC)(cylinder(d = screw_d, h = 10)))

    scad_render_to_file(model, '_%s.scad'% __file__.split('/')[-1][:-3])

