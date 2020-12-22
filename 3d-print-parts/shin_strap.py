from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

t = 2.5

def platform_with_holes(x, y):
    model = cube([x, y, t])
    
    hole_d = 3.5
    hole_offset = 1.7
    for a in [hole_offset + (hole_d / 2), y - hole_offset - (hole_d / 2)]:
        model -= translate([4, a])(cylinder(d = hole_d, h = t))

    return model

def strap():
    h = 90.0
    model = hull()(cylinder(d = 80) + up(h)(cylinder(d = 120)))
    model *= translate([-h, 10])(cube(h * 2))

    sf = 0.95
    model -= super_hole(translate([0, -1, -1])(scale([sf, sf, 1.1])(model)), 'leg_hole')

    model = minkowski()(sphere(r = 1), model)

    holes = cube([200, 5, 25])
    holes += up(h - 40)(holes)
    holes = translate([-100, 15, 10])(holes)

    model -= super_hole(holes, 'strap_hole')

    return model

def component_block():
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
            + background(translate([-10, 36, -23])(cube([63, 10, 67])))
        )
        + translate([4, 70, 37])(
            pcb_holder
            + translate([7, -40])(cube([18, 40, 10]))
        )
    )

    model -= strap()

    return model

if __name__ == '__main__':
    model = strap()

    scad_render_to_file(model, '_%s.scad'% __file__[:-3])
