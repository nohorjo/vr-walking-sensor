from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

from shin_strap import *

if __name__ == '__main__':
    big_x = 10.5
    big_y = 32.0
    small_y = 22.0

    pcb_holder = platform_with_holes(big_x, big_y)
    pcb_holder += translate([big_x, (big_y - small_y) / 2, t])(
        rotate(90, BACK_VEC)(platform_with_holes(8.0, small_y)
    ))

    pcb_holder = rotate(90, BACK_VEC)(pcb_holder)
    pcb_holder = rotate(90, DOWN_VEC)(pcb_holder)

    model = translate([-20, 15, 10])(
        rotate(12.5, LEFT_VEC)(
            cube([40, 35, 35])
            + right(11)(cube([18, 35, 55]))
        )
        + translate([4, 70, 37])(
            pcb_holder
            + translate([7, -40])(cube([18, 40, 10]))
        )
    )

    model -= strap()

    scad_render_to_file(model, '_%s.scad'% __file__.split('/')[-1][:-3])

