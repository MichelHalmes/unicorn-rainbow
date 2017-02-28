# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import random

from rpi_ws281x.python.neopixel import Color, Adafruit_NeoPixel
from collections import OrderedDict


from math import cos, pi
def wheel(deg):
    red   = cos(deg      *pi/180) * 127 + 128
    green = cos((deg+120)*pi/180) * 127 + 128
    blue  = cos((deg+240)*pi/180) * 127 + 128
    return (red, green, blue)


RAINBOW_RGB = map(wheel, range(360))


" PARTS INITIALIZATION "
# LED strip configuration:
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 155     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
RAINBOW_PARTS  =  [
    ('violet',  {'offset': 0, 'length': 37, 'is_reverse': False, 'base_rgb': RAINBOW_RGB[330]}),
    ('blue',    {'offset': 0, 'length': 32, 'is_reverse': True,  'base_rgb': RAINBOW_RGB[270]}),
    ('green',   {'offset': 1, 'length': 55, 'is_reverse': False, 'base_rgb': RAINBOW_RGB[210], 'is_double_dense': True}),
    ('yellow',  {'offset': 1, 'length': 24, 'is_reverse': True,  'base_rgb': RAINBOW_RGB[150]}),
    ('orange',  {'offset': 0, 'length': 20, 'is_reverse': False, 'base_rgb': RAINBOW_RGB[90]}),
    ('red',     {'offset': 0, 'length': 15, 'is_reverse': True,  'base_rgb': RAINBOW_RGB[30]}),
]

" SPEED PARAMETERS "
WAIT_MS = 50
SPEED_MS = 200
NORMAL_STEP_PERIOD = int(round(SPEED_MS/WAIT_MS))
MAX_PART_LEN = max(map(lambda tup: tup[1]['length'], RAINBOW_PARTS))
NB_PARTS =len(RAINBOW_PARTS)
CYCLE_NB_STEPS = MAX_PART_LEN*NORMAL_STEP_PERIOD



class Rainbow(object):
    def __init__(self):

        self._parts = []
        start_idx = 0
        part_idx = 0
        for name, parts_dict in RAINBOW_PARTS:
            start_idx += parts_dict['offset']
            part = Part(name, start_idx, part_idx, parts_dict)
            start_idx += parts_dict['length']
            part_idx += 1

            self._parts.append(part)

        self._strip = Adafruit_NeoPixel(start_idx, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self._strip.begin()
        self._anim_data = {}

    def render_parts(self):
        for part in self._parts:
            part.render(self._strip)

        self._strip.show()


    def animation(self, anim_func, reset_rgb, nb_cycles=3):
        self._anim_data = {}
        for part in self._parts:
            part.set_uniform_color(reset_rgb)
            part._anim_data = {}

        for step in range(nb_cycles*CYCLE_NB_STEPS):
            for part in self._parts:
                anim_func(part, step)

            self.render_parts()
            time.sleep(WAIT_MS/1000.0)

    def a_colorwipe(self, part, step):
        pixel_idx = int(step * part._length / CYCLE_NB_STEPS) % part._length
        if pixel_idx == 0:
            part.set_uniform_color((0,0,0))

        part.set_pixel_color(pixel_idx)

    def a_flashparts(self, part, step):
        if step % NORMAL_STEP_PERIOD != 0:
            return

        periods = step/NORMAL_STEP_PERIOD

        if (periods+part._part_idx) % 2 == 0:
            part.set_uniform_color()
        else:
            part.set_uniform_color((0,0,0))

    def a_gradients(self, part, step):
        RAINBOW_LEN = len(RAINBOW_RGB)
        start_idx = step % RAINBOW_LEN
        leds_rgb = [RAINBOW_RGB[int(start_idx + (led_idx*RAINBOW_LEN/part._length))%RAINBOW_LEN] for led_idx in range(part._length)]
        part.set_leds_rgb(leds_rgb)


    def a_commet(self, part, step):
        if step % NORMAL_STEP_PERIOD != 0:
            return

        if len(part._anim_data) == 0:
            start_pixel = random.randint(int(0.2*part._length), int(0.8*part._length))
            part._anim_data = {'left_pix': start_pixel, 'right_pix': start_pixel}
            part.set_pixel_color(start_pixel, (200,200,200))
        else:
            left_pix = part._anim_data['left_pix']
            right_pix = part._anim_data['right_pix']
            part.set_pixel_color(left_pix)
            part.set_pixel_color(right_pix)
            is_done = True
            if left_pix > 0:
                left_pix -= 1
                part.set_pixel_color(left_pix, (250,250,250))
                part._anim_data['left_pix'] = left_pix
                is_done = False
            if right_pix < part._length-1:
                right_pix += 1
                part.set_pixel_color(right_pix, (250,250,250))
                part._anim_data['right_pix'] = right_pix
                is_done = False

            if is_done:
                part._anim_data = {}



class Part(object):
    def __init__(self, name, start_idx, part_idx, part_dict):
        self._name = name
        self._start_idx = start_idx
        self._part_idx = part_idx
        self._length = part_dict['length']
        self._is_reverse = part_dict['is_reverse']
        self._base_rgb = part_dict['base_rgb']
        self._is_double_dense = part_dict.get('is_double_dense', False)
        self._leds_rgb = [self._base_rgb] * self._length
        self._anim_data = {}

    def render(self, strip):
        start = self._start_idx
        end = start + self._length
        step = 1 if not self._is_double_dense \
                else 2
        if self._is_reverse:
            strip.setPixelColor(slice(start,end, step), map(lambda rgb: Color(*rgb), reversed(self._leds_rgb)))
        else:
            strip.setPixelColor(slice(start,end, step), map(lambda rgb: Color(*rgb), self._leds_rgb))


    def set_uniform_color(self, rgb = None):
        rgb = self._base_rgb  if rgb is None else rgb
        self._leds_rgb = [rgb] * self._length

    def set_pixel_color(self, pixel, rgb = None):
        rgb = self._base_rgb  if rgb is None else rgb
        self._leds_rgb[pixel] = rgb

    def set_leds_rgb(self, leds_rgb):
        assert len(leds_rgb) == self._length
        self._leds_rgb = leds_rgb




# Main program logic follows:
if __name__ == '__main__':
    rainbow = Rainbow()
    rainbow.render_parts()
    time.sleep(100)

    rainbow.animation(rainbow.a_gradients, (0,0,0), 4)
    rainbow.animation(rainbow.a_colorwipe, (0,0,0), 3)
    rainbow.animation(rainbow.a_commet, None, 5)
    rainbow.animation(rainbow.a_flashparts, (0,0,0), 5)
