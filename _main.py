
from _base_classes import Rainbow
import time

from mich_animations import *


if __name__ == '__main__':
    rainbow = Rainbow()
    # rainbow.render_parts()
    # time.sleep(10)

    Feynman(rainbow, 1 ,10).run_animation()
    SwipeLeftRight(rainbow, 1 ,1).run_animation()
    Gradients(rainbow, 1 ,1).run_animation()
    SwipeUpDown(rainbow, 1 ,1).run_animation()
    
	
