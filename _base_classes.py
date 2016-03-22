import time
import random

from rpi_ws281x.python.neopixel import Color, Adafruit_NeoPixel
from collections import OrderedDict


# from math import cos, pi
# def wheel(deg):
#     red   = cos(deg      *pi/180) * 127 + 128
#     green = cos((deg+120)*pi/180) * 127 + 128
#     blue  = cos((deg+240)*pi/180) * 127 + 128
#     return (int(red), int(green), int(blue))

import colorsys
def wheel(deg):
    rgb = colorsys.hsv_to_rgb((deg/360.0)**2, 1, 1)
    return tuple(int(255*c/sum(rgb)) for c in rgb) 


RAINBOW_RGB = map(wheel, range(360))


" PARTS INITIALIZATION "
# LED strip configuration:
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM! => 13 or 18).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 155     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
RAINBOW_PARTS  =  [
    ('violet',  {'offset': 0, 'length': 37, 'is_reverse': False, 'base_rgb': RAINBOW_RGB[330]}),
    ('blue',    {'offset': 0, 'length': 32, 'is_reverse': True,  'base_rgb': RAINBOW_RGB[270]}),
    ('green',   {'offset': 0, 'length': 29, 'is_reverse': False, 'base_rgb': RAINBOW_RGB[210], 'led_step': 2}),
    ('yellow',  {'offset': 0, 'length': 24, 'is_reverse': True,  'base_rgb': RAINBOW_RGB[150]}),
    ('orange',  {'offset': 0, 'length': 20, 'is_reverse': False, 'base_rgb': RAINBOW_RGB[90]}),
    ('red',     {'offset': 0, 'length': 16, 'is_reverse': True,  'base_rgb': RAINBOW_RGB[30]}),
]

" SPEED PARAMETERS "
WAIT_MS = 50
SPEED_MS = 200
# Convention for the period (in number of animation-steps) at which animations can introduce "big" changes
# (to avoid the animations being confused with uncontrolled flickering...)
NORMAL_NB_STEPS_PER_STABLE_PERIOD = int(round(SPEED_MS/WAIT_MS))
MAX_PART_LEN = max(map(lambda tup: tup[1]['length'], RAINBOW_PARTS))
NB_PARTS =len(RAINBOW_PARTS)
NORMAL_NB_STEPS_PER_CYCLE = MAX_PART_LEN*NORMAL_NB_STEPS_PER_STABLE_PERIOD

class Rainbow(object):
    def __init__(self):
        self._parts = []
        start_idx = 0
        part_idx = 0
        for name, parts_dict in RAINBOW_PARTS:
            start_idx += parts_dict['offset']
            part = Part(name, start_idx, part_idx, parts_dict)
            start_idx += (part._length - 1)* part._led_step + 1
            part_idx += 1

            self._parts.append(part)

        self._strip = Adafruit_NeoPixel(start_idx, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self._strip.begin()

    def render_parts(self):
        for part in self._parts:
            part.render(self._strip)

        self._strip.show()


    def run_animation(self, animation):
        for part in self._parts:
            part.set_uniform_color(animation.RESET_RGB)
            part._anim_data = {}

        for step_cnt in range(animation.get_nb_steps()):
            for part in self._parts:
                animation.run_step(part, step_cnt)

            self.render_parts()
            time.sleep(WAIT_MS/1000.0)


class Part(object):
    def __init__(self, name, start_idx, part_idx, part_dict):
        self._name = name
        self._start_idx = start_idx
        self._part_idx = part_idx
        self._length = part_dict['length']
        self._is_reverse = part_dict['is_reverse']
        self._base_rgb = part_dict['base_rgb']
        self._led_step = part_dict.get('led_step', 1)
        self._leds_rgb = [self._base_rgb] * self._length
        self._anim_data = {}

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


    def set_pixel_color(self, pixel, rgb = None):
        rgb = self._base_rgb  if rgb is None else rgb
        self._leds_rgb[pixel] = rgb

    def set_leds_rgb(self, leds_rgb):
        assert len(leds_rgb) == self._length
        self._leds_rgb = leds_rgb




class Animation(object):
    NORMAL_NB_STEPS_PER_CYCLE = NORMAL_NB_STEPS_PER_CYCLE
    NORMAL_NB_STEPS_PER_STABLE_PERIOD = NORMAL_NB_STEPS_PER_STABLE_PERIOD
    RAINBOW_RGB = RAINBOW_RGB

    RESET_RGB = "Define in BaseClass"
    NB_CYCLES_PER_ANIMATION = "Define in BaseClass"

    def __init__(self, speed, duration):
        self._speed = speed
        self._duration = duration

    def get_nb_steps(self):
        return self._duration * self.NB_CYCLES_PER_ANIMATION * self.NORMAL_NB_STEPS_PER_CYCLE

    def run_step(self, part, step_cnt):
        raise NotImplementedError('')
