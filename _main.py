from _base_classes import Rainbow
import time
import random

from animations import *

ANIMATIONS = [
    Surface2D,
    Pendulum,
    TextBanner,
    Gradients,
    Snake,
    Feynman,
    SwipeLeftRight,   
    SwipeUpDown,
]


if __name__ == '__main__':
    rainbow = Rainbow()

    Surface2D(rainbow).run_animation()



    # TOTAL_VARIETY = sum([anim.VARIETY for anim in ANIMATIONS])
    
    # while True:
    #     treshold_proba = random.random()
    #     cum_proba = 0
    #     for anim in ANIMATIONS:
    #         cum_proba+= (1.*anim.VARIETY/TOTAL_VARIETY)
    #         if cum_proba >= treshold_proba:
    #             break
    #     print anim.__name__
    #     anim(rainbow).run_animation()
        
        
        
    
	
