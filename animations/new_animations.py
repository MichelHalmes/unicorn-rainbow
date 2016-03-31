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

    FUNCTIONS = {}

    # PLAN
    def get_value_fun():
        sign = random.choice([-1, +1])
        mult = random.choice([1, 2, 3])
        def value_f(x, y, rot): 
            return math.sin(2.*math.pi*rot)*y + sign*math.cos(2.*math.pi*rot*mult)*x
        return value_f 
    value_range = 2*math.sqrt(2) # min = max = math.sin(math.pi/4) + math.cos(math.pi/4)
    FUNCTIONS['plan'] = (value_range, get_value_fun())

    # CIRCLE
    def get_value_fun():
        sign = random.choice([-1, +1, +1])
        exp = random.choice([1, 2, 2, 3])
        def value_f(x, y, rot): 
            return x**exp + sign*y**exp + 2*rot
        return value_f
    value_range = 2
    FUNCTIONS['circle'] = (value_range, get_value_fun())

    # ELLIPSE
    def get_value_fun():
        sign = random.choice([-1, +1, +1])
        ex_centr =  random.choice([2, 3])
        e_oscil = random.choice([0, .1, .3])
        value_range = 1+ex_centr**2 
        def value_f(x, y, rot): 
            e_scale = (1+e_oscil*math.sin(2.*math.pi*rot))
            return x**2 + sign * (y*ex_centr*e_scale)**2 + value_range*rot
        return (value_range, value_f)
    FUNCTIONS['ellipse'] = get_value_fun()

    # # TRIGONOMETRY
    # def get_value_fun():
    #     sign = 1# random.choice([-1, +1, +1])
    #     exp = 1 #random.choice([1, 2, 2, 3])
    #     def value_f(x, y, rot): 
    #         return  math.sin(2.*math.pi*(x)) + math.sin(2.*math.pi*(y)) + math.sin(2.*math.pi*(rot))
    #     return value_f
    # value_range = 2
    # FUNCTIONS['trigonometry'] = (value_range, get_value_fun())
 

    def __init__(self, rainbow, speed, duration):
        super(self.__class__, self).__init__(rainbow, speed, duration)

        palette_name = 'gist_rainbow' #random.choice(self.COLOR_PALETTES.keys())
        self._palette = self.COLOR_PALETTES[palette_name]

        function_name = 'trigonometry' # random.choice(self.FUNCTIONS.keys())
        self._function = self.FUNCTIONS[function_name]

        print "Palette: %s; Function: %s" % (palette_name, function_name)

        self._rpm = 20

    def get_part_rgb_fun(self, part, step_cnt):
        rotations = 1.*self._rpm*step_cnt*self.WAIT_MS/(1000*60)

        part_pct = 1.*part._id/(self.NB_RAINBOW_PARTS-1)
        x = (part_pct)*2-1  # [-1, 1]
        
        value_range, value_f = self._function
        def rgb(led_idx):
            led_pct = 1.*led_idx/(part._length-1)
            y = led_pct*2-1 # [-1, 1]
            value = value_f(x, y, rotations)
            value_pct = value  / value_range
            palette_idx = int(round(value_pct*(len(self._palette)-1))) % len(self._palette)
            return self._palette[palette_idx]

        return rgb



    def run_step(self, part, step_cnt):

        rgb = self.get_part_rgb_fun(part, step_cnt)

        leds_rgb = [rgb(led_idx) for led_idx in range(part._length)]
        part.set_leds_rgb(leds_rgb)


