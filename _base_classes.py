import time
import random
import colorsys
import math
import json

from rpi_ws281x.python.neopixel import Color, Adafruit_NeoPixel


def hsv_deg_to_rgb(deg):
    return tuple(int(255*c) for c in colorsys.hsv_to_rgb(deg/360.0, 1, 1)) 

" PARTS INITIALIZATION "
# LED strip configuration:
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM! => 13 or 18).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 60     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
RAINBOW_PARTS  =  [
    ('violet',  {'offset': 0, 'length': 37, 'is_reverse': False, 'base_rgb': hsv_deg_to_rgb(300) }),
    ('blue',    {'offset': 0, 'length': 32, 'is_reverse': True,  'base_rgb': hsv_deg_to_rgb(240) }),
    ('green',   {'offset': 0, 'length': 29, 'is_reverse': False, 'base_rgb': hsv_deg_to_rgb(120) , 'led_step': 2}),
    ('yellow',  {'offset': 0, 'length': 24, 'is_reverse': True,  'base_rgb': hsv_deg_to_rgb(060) }),
    ('orange',  {'offset': 0, 'length': 20, 'is_reverse': False, 'base_rgb': hsv_deg_to_rgb(030) }),
    ('red',     {'offset': 0, 'length': 16, 'is_reverse': True,  'base_rgb': hsv_deg_to_rgb(000) }),
]

" SPEED PARAMETERS "
WAIT_MS = 20

class Rainbow(object):
    def __init__(self):
        self._parts = []
        start_idx = 0
        part_id = 0
        for name, parts_dict in RAINBOW_PARTS:
            start_idx += parts_dict['offset']
            part = Part(name, start_idx, part_id, parts_dict)
            start_idx += (part._length - 1)* part._led_step + 1
            part_id += 1

            self._parts.append(part)

        self._strip = Adafruit_NeoPixel(start_idx, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self._strip.begin()

    def render_parts(self):
        for part in self._parts:
            part.render(self._strip)

        self._strip.show()


    
class Part(object):
    def __init__(self, name, start_idx, part_id, part_dict):
        self._name = name
        self._start_idx = start_idx
        self._id = part_id
        self._length = part_dict['length']
        self._is_reverse = part_dict['is_reverse']
        self._base_rgb = part_dict['base_rgb']
        self._led_step = part_dict.get('led_step', 1)
        self._leds_rgb = [self._base_rgb] * self._length

    def render(self, strip):
        start = self._start_idx
        end = start + self._length * self._led_step
        if self._is_reverse:
            strip.setPixelColor(slice(start,end,self._led_step), map(lambda rgb: Color(*rgb), reversed(self._leds_rgb)))
        else:
            strip.setPixelColor(slice(start,end,self._led_step), map(lambda rgb: Color(*rgb), self._leds_rgb))


    def set_uniform_color(self, rgb = None):
        rgb = self._base_rgb  if rgb is None else rgb
        self._leds_rgb = [rgb] * self._length


    def set_led_color(self, led_idx, rgb = None):
        rgb = self._base_rgb  if rgb is None else rgb
        self._leds_rgb[led_idx] = rgb

    def set_leds_rgb(self, leds_rgb):
        assert len(leds_rgb) == self._length
        self._leds_rgb = leds_rgb



class Animation(object):
    # Convention for the period (in number of animation-steps) at which animations can introduce "big" changes
    # (to avoid the animations being confused with uncontrolled flickering...)
    WAIT_MS = WAIT_MS
    SPEED_MS = 100
    NORMAL_NB_STEPS_PER_STABLE_PERIOD = int(round(SPEED_MS/WAIT_MS))
    MAX_PART_LEN = max(map(lambda tup: tup[1]['length'], RAINBOW_PARTS))
    NB_RAINBOW_PARTS =len(RAINBOW_PARTS)
    NORMAL_NB_STEPS_PER_CYCLE = MAX_PART_LEN*NORMAL_NB_STEPS_PER_STABLE_PERIOD

    with open('./palettes/color_palettes.json', 'r') as fp:
        COLOR_PALETTES = json.load(fp)

    RESET_RGB = "Define in BaseClass"
    NB_CYCLES_PER_ANIMATION = "Define in BaseClass"

    def __init__(self, rainbow, speed, duration):
        self._rainbow = rainbow
        self._speed = speed
        assert self._speed > 0
        self._duration = duration
        self._cnst_angular_speed = False
        self._parts_data = {-1: {}} 
        for part in self.get_parts():
            self._parts_data[part._id] = {'prev_period': -1}



    def get_parts(self):
        return self._rainbow._parts

    def get_data(self, part=None):
        idx = part._id if part is not None else -1
        return self._parts_data[idx]


    def get_nb_steps(self):
        return self._duration * self.NB_CYCLES_PER_ANIMATION * self.NORMAL_NB_STEPS_PER_CYCLE

    def run_parts_step(self, step_cnt):
        for part in self.get_parts():
            self.run_step(part, step_cnt)

        if step_cnt % self.NORMAL_NB_STEPS_PER_STABLE_PERIOD == 0:
            self.run_parts_period(step_cnt)

        
    def run_step(self, part, step_cnt):
        pass

    def run_parts_period(self, step_cnt):
        for part in self.get_parts():
            period_cnt = int(self.get_period_cnt(part, step_cnt))
            if period_cnt != self.get_data(part)['prev_period']:
                self.run_period(part, period_cnt)
                self.get_data(part)['prev_period'] = period_cnt

        
    def run_period(self, part, period_cnt):
        pass

    
    def get_period_cnt(self, part, step_cnt):
        period_cnt = 1.*step_cnt/self.NORMAL_NB_STEPS_PER_STABLE_PERIOD
        if self._cnst_angular_speed:
            period_cnt *= 1.*part._length/self.MAX_PART_LEN

        return period_cnt


    def run_animation(self):
        for part in self.get_parts():
            part.set_uniform_color(self.RESET_RGB)

        try:
            for step_cnt in range(self.get_nb_steps()):
                self.run_parts_step(step_cnt)

                self._rainbow.render_parts()
                time.sleep(WAIT_MS/1000.0)
        except StopIteration:
            pass

    # @staticmethod
    # def hsv_deg_to_rgb(deg, sat, val):
    #     assert sat>=0 and sat<=1
    #     assert val>=0 and val<=1
    #     return tuple(int(255*c) for c in colorsys.hsv_to_rgb(deg/360.0, sat, val)) 

    








