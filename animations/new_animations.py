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



class Surface2D(Animation):
    RESET_RGB = (0,0,0)
    NB_CYCLES_PER_ANIMATION = 2
 

    def __init__(self, rainbow, speed, duration):
        super(self.__class__, self).__init__(rainbow, speed, duration)

        palette_name = 'mich_rainbow' #random.choice(self.COLOR_PALETTES.keys())
        print palette_name
        self._palette = self.COLOR_PALETTES[palette_name]
        self._rpm = 20

    def get_part_rgb_fun(self, part, step_cnt):
        rotations = 1.*self._rpm*step_cnt*self.WAIT_MS/(1000*60)
        angle = 2.*math.pi*rotations

        part_pct = 1.*part._id/(self.NB_RAINBOW_PARTS-1)
        x = (part_pct)*2 - 1 # [-1, 1]
        min_val = -2.
        max_val = 2.
        def rgb_fun(led_idx):
            led_pct = 1.*led_idx/(part._length-1)
            y = led_pct*2 - 1 # [-1, 1]
            val = y - math.tan(angle)*x
            val_pct = (val - min_val) / (max_val - min_val)
            palette_idx = int(round(val_pct*(len(self._palette)-1))) % len(self._palette)
            return self._palette[palette_idx]

        return rgb_fun



    def run_step(self, part, step_cnt):

        rgb_fun = self.get_part_rgb_fun(part, step_cnt)

        leds_rgb = [rgb_fun(led_idx) for led_idx in range(part._length)]
        part.set_leds_rgb(leds_rgb)


