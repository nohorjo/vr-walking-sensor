from solid import *
from solid.utils import *

from constants import *
from moveable_point import *
from super_hole import *

from shin_strap import *

if __name__ == '__main__':
    model = component_block(False)
    scad_render_to_file(model, '_%s.scad'% __file__[:-3])

