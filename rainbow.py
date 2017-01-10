# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import random

from rpi_ws281x.python.neopixel import Color, Adafruit_NeoPixel
from collections import OrderedDict


# LED strip configuration:
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 80     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
RAINBOW_PARTS  =  [
    ('violet',   {'offset': 2, 'length': 7, 'is_reverse': False, 'basecolor': (100,50,255)}),
    ('blue',     {'offset': 2, 'length': 8, 'is_reverse': True, 'basecolor': (0,0,255)}),
    ('green',    {'offset': 2, 'length': 7, 'is_reverse': False, 'basecolor': (0,255,0)}),
    ('yellow',   {'offset': 2, 'length': 10, 'is_reverse': True, 'basecolor': (10,155,0)}),
    ('orange',   {'offset': 2, 'length': 8, 'is_reverse': False, 'basecolor': (128,128,0)}),
    ('red',      {'offset': 2, 'length': 7, 'is_reverse': True, 'basecolor': (255,0,0)}),    
]


                    

class Rainbow(object):
    def __init__(self):

        self._parts = []
        start_idx = 0
        for name, parts_dict in RAINBOW_PARTS:
            start_idx += parts_dict['offset']
            part = Part(name, start_idx, parts_dict['length'], parts_dict['is_reverse'], parts_dict['basecolor'])
            start_idx += parts_dict['length']
            
            self._parts.append(part)

        self._strip = Adafruit_NeoPixel(start_idx, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self._strip.begin()
        self._anim_data = {}

    def render_parts(self):
        for part in self._parts:
            part.render(self._strip)
           
        self._strip.show()

    WAIT_MS = 50
    def animation(self, anim_func, reset_rgb, duration_ms=2000):
        self._anim_data = {}
        for part in self._parts:
            part.set_uniform_color(reset_rgb)
            part._anim_data = {}

        nb_steps = int(duration_ms/WAIT_MS)
        for step in range(nb_steps):
            for part_idx, part in enumerate(self._parts):
                anim_func(part, part_idx, step, nb_steps)

            self.render_parts()
            time.sleep(WAIT_MS/1000.0)

    def a_colorwipe(part, part_idx, step, nb_steps): 
        pixel_idx = int(step * part._length / nb_steps)
        part.set_pixel_color(pixel_idx)
            

    def a_commet(part, part_idx, step, nb_steps):
        if len(part._anim_data == 0):
            start_pixel = random.randint(int(0.1*part._length), int(0.9*part._length))
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
    def __init__(self, name, start_idx, length, is_reverse, base_rgb):
        self._name = name
        self._start_idx = start_idx
        self._length = length
        self._is_reverse = is_reverse
        self._base_rgb = base_rgb
        self._leds_rgb = [base_rgb] * length
        self._anim_data = {}

    def render(self, strip):
        start = self._start_idx
        end = start + self._length
        if self._is_reverse:
            strip.setPixelColor(slice(start,end), map(lambda rgb: Color(*rgb), reversed(self._leds_rgb)))
        else:
            strip.setPixelColor(slice(start,end), map(lambda rgb: Color(*rgb), self._leds_rgb))


    def set_uniform_color(self, rgb = None):
        rgb = self._base_rgb  if rgb is None else rgb
        self._leds_rgb = [rgb] * self._length

    def set_pixel_color(self, pixel, rgb = None):
        rgb = self._base_rgb  if rgb is None else rgb
        self._leds_rgb[pixel] = rgb




# Main program logic follows:
if __name__ == '__main__':
    rainbow = Rainbow()
    rainbow.render_parts()
    time.sleep(1)

    rainbow.animation(a_colorwipe, (0,0,0))
    rainbow.animation(a_commet, None)


