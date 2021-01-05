from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

if __name__ == '__main__':
    model = circle(d = 42)
    model -= circle(d = 28.5)
    model -= translate([-25, 11])(square(50))
    model -= right(17)(circle(d = 3.5))
    model -= left(17)(circle(d = 3.5))

    model = linear_extrude(6)(model)

    tube_part = cylinder(d = tube_d + 4, h = 7) - cylinder(d = tube_d, h = 10)

    model += translate([-20, 10, 8.5])((rotate(90, FORWARD_VEC)(tube_part)))

    model += translate([0, -16, 3])(
        minkowski()(cube([30, 4, 6], True), rotate(90, LEFT_VEC)(cylinder(d = 10, h = 0.1)))
    )
    model -= back(23)(cube([25, 10, 20], True))

    scad_render_to_file(model, '_%s.scad'% __file__.split('/')[-1][:-3])

