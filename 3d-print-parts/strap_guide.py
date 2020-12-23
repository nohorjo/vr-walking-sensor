from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

if __name__ == '__main__':
    model = minkowski()(
        cube([70, 6, 1]),
        cylinder(d = 4, h = 1)
    )

    scad_render_to_file(model, '_%s.scad'% __file__[:-3])

