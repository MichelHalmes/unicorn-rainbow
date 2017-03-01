
from _base_classes import Rainbow
import time

from mich-animations import *


if __name__ == '__main__':
    rainbow = Rainbow()
    rainbow.render_parts()
    time.sleep(2)

    rainbow.run_animation(Gradients(0,0))
    rainbow.animation(Colorwipe(0,0))
    rainbow.animation(Commet(0,0))
    rainbow.animation(Flashparts(0,0))
