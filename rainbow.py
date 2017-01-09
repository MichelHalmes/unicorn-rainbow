# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

from rpi_ws281x.python.neopixel import Color, Adafruit_NeoPixel
from collections import OrderedDict


# LED strip configuration:
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 80     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
RAINBOW_PARTS  =  [
    ('red',      {'offset': 2, 'length': 3, 'basecolor': (255,0,0)}),
    ('orange',   {'offset': 2, 'length': 4, 'basecolor': (128,128,0)}),
    ('yellow',   {'offset': 2, 'length': 5, 'basecolor': (10,155,0)}),
    ('green',    {'offset': 2, 'length': 6, 'basecolor': (0,255,0)}),
    ('blue',     {'offset': 2, 'length': 7, 'basecolor': (0,0,255)}),
    ('violet',   {'offset': 2, 'length': 8, 'basecolor': (50,50,255)})
]
                    

class Rainbow(object):
    def __init__(self):

        self._parts = []
        start_idx = 0
        for name, parts_dict in RAINBOW_PARTS:
            start_idx += parts_dict['offset']
            part = Parts(name, start_idx, parts_dict['length'], parts_dict['basecolor'])
            start_idx += parts_dict['length']
            
            self._parts.append(part)


        self._strip = Adafruit_NeoPixel(start_idx, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self._strip.begin()

    def render_parts(self):
        for part in self._parts:
            part.render(self._strip)
           
        self._strip.show()

            

class Part(object):
    def __init__(self, name, start_idx, length, base_rgb):
        self._name = name
        self._start_idx = start_idx
        self._length = length
        self._leds_rgb = [base_rgb] * length

    def render(self, strip):
        start = self._start_idx
        end = start + self._length
        strip.setPixelColor(slice(start,end), map(lambda  rgb: Color(*rgb), self._led_rgbs))




# Main program logic follows:
if __name__ == '__main__':
    Rainbow().render_parts()


