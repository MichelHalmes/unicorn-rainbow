import random
import math

from _base_classes import Animation

class Basic(Animation):
    RESET_RGB = (0,0,0)
    NB_CYCLES_PER_ANIMATION = 2

    def __init__(self, rainbow, speed, duration):
        super(self.__class__, self).__init__(rainbow, speed, duration)
        self._cnst_angular_speed = random.choice([False, True])
        self._synchronize_parts = random.choice([False, True])



    def run_period(self, part, period_cnt):
       
        # part.set_uniform_color()

        # color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        # print color

        # [part.set_led_color(idx, color) \
        #     for idx in range(, int(part._length*0.7))]
        part.set_led_color(int(round(part._length*0.1)), (200,200,200))
        part.set_led_color(int(round(part._length*0.3)), (200,200,200))
        part.set_led_color(int(round(part._length*0.5)), (200,200,200))
        part.set_led_color(int(round(part._length*0.7)), (200,200,200))
        part.set_led_color(int(round(part._length*0.9)), (200,200,200))




