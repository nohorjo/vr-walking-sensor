from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

if __name__ == '__main__':
    x = 90.0
    switch_x = 17.0
    switch_y = 7.0
    t = 2.5
    strap_gap = 4.5

    p = MoveablePoint()
    model = linear_extrude(16)(polygon([
        p.val(),
        p.right(x).val(),
        p.up(strap_gap + (2 * t)).val(),
        p.left(((x - switch_x) / 2) - strap_gap - t).val(),
        p.down(t).val(),
        p.right(((x - switch_x) / 2) - (t * 2) - strap_gap).val(),
        p.down(strap_gap).val(),

        p.left(((x - (t * 2)) / 2) - (switch_x / 2) - t).val(),
        p.up(switch_y).val(),
        p.left(t).val(),
        p.down(switch_y).val(),
        p.left(switch_x).val(),
        p.up(switch_y).val(),
        p.left(t).val(),
        p.down(switch_y).val(),
        p.left(((x - (t * 2)) / 2) - (switch_x / 2) - t).val(),

        p.up(strap_gap).val(),
        p.right(((x - switch_x) / 2) - (t * 2) - strap_gap).val(),
        p.up(t).val(),
        p.left(((x - switch_x) / 2) - strap_gap - t).val(),
    ]))
    
    scad_render_to_file(model, '_%s.scad'% __file__[:-3])

