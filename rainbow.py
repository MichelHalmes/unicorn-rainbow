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
LED_SIZES      =  {'red':       {'offset': 2, 'length': 3, 'idx': 0, 'basecolor': (255,0,0)},
                    'orange':   {'offset': 2, 'length': 4, 'idx': 1, 'basecolor': (128,128,0)},
                    'yellow':   {'offset': 2, 'length': 5, 'idx': 2, 'basecolor': (10,155,0)},
                    'green':    {'offset': 2, 'length': 6, 'idx': 3, 'basecolor': (0,255,0)},
                    'blue':     {'offset': 2, 'length': 7, 'idx': 4, 'basecolor': (0,0,255)},
                    'violet':   {'offset': 2, 'length': 8, 'idx': 5, 'basecolor': (50,50,255)}
                    }

class Rainbow(object):
    def __init__(self):

        


        self._repr = OrderedDict([('red', []), ('orange', []), ('yellow', []), ('green', []), ('blue', []), ('violet', [])])
        start_idx = 0
        for spectrum, led_rgbs in self._repr.items():
            print spectrum
            rgb = LED_SIZES[spectrum]['basecolor']
            length = LED_SIZES[spectrum]['length']
            start_idx += LED_SIZES[spectrum]['offset']
            LED_SIZES[spectrum]['start_idx'] = start_idx
            start_idx +=length
            
            self._repr[spectrum] = [rgb]*length


        self._strip = Adafruit_NeoPixel(start_idx, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self._strip.begin()

        for spectrum, led_rgbs in self._repr.items():
            start = LED_SIZES[spectrum]['start_idx']
            end = start + LED_SIZES[spectrum]['length']
            self._strip.setPixelColor(slice(start,end)  , map(lambda  rgb: Color(rgb[0], rgb[1], rgb[2]), led_rgbs))

        self._strip.show()

            





        




# Main program logic follows:
if __name__ == '__main__':
    Rainbow()

