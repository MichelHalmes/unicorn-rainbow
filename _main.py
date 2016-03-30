from _base_classes import Rainbow
import time

from mich_animations import *
from new_animations import *


if __name__ == '__main__':
    rainbow = Rainbow()
    # rainbow.render_parts()
    # time.sleep(10)

    Pendulum(rainbow, 1 ,1).run_animation()
    # while True:
        # Snake(rainbow, 1 ,2).run_animation()
        # Feynman(rainbow, 1 ,1).run_animation()
        # SwipeLeftRight(rainbow, 1 ,1).run_animation()
        # Gradients(rainbow, 1 ,1).run_animation()
        # SwipeUpDown(rainbow, 1 ,1).run_animation()
    
	
