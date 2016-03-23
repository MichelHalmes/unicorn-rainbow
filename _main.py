
from _base_classes import Rainbow
import time

from mich_animations import *


if __name__ == '__main__':
    rainbow = Rainbow()
    # rainbow.render_parts()
    # time.sleep(10)

    

    rainbow.run_animation(Gradients(1,1))
    rainbow.run_animation(Flashparts(1,1))
    rainbow.run_animation(Colorwipe(1,1))
    rainbow.run_animation(Commet(1,1))
	
