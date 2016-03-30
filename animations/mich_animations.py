import random
import math
import colorsys

from _base_classes import Animation




class Feynman(Animation):
    RESET_RGB = None
    NB_CYCLES_PER_ANIMATION = 1

    def __init__(self, rainbow, speed, duration):
        super(self.__class__, self).__init__(rainbow, speed, duration)

        if random.random() < 0.5:
            self.run_step = self.run_interval
        else:
            self.run_period = self.run_interval

        
        [self.initialize_part_data(part) for part in self.get_parts()]

    def initialize_part_data(self, part):
        part_data = self.get_data(part)
        if 'dots' not in part_data:
            part_data['dots'] = []

        start_idx = self.get_start_idx(part)
        self.get_data(part)['dots'].append({'left_idx': start_idx, 'right_idx': start_idx})

    def get_start_idx(self, part):
        dots_data = self.get_data(part)['dots']
        if len(dots_data) == 0:
            start_idx = random.randint(int(0.25*part._length), int(0.75*part._length))
        else:
            low = max(0, dots_data[-1]['left_idx'])
            high = min(part._length, dots_data[-1]['right_idx'])
            start_idx = int(random.triangular(low, high))
        return start_idx

    def run_interval(self, part, _):
        part.set_uniform_color()

        dots_data = self.get_data(part)['dots']

        if dots_data[-1]['right_idx'] - dots_data[-1]['left_idx'] > 10:
            if random.random() < 0.07:
                start_idx = self.get_start_idx(part)
                dots_data.append({'left_idx': start_idx, 'right_idx': start_idx})

        for dot in dots_data:
            left_idx  = dot['left_idx']  - 1
            right_idx = dot['right_idx'] + 1

            dot['left_idx'] = left_idx
            dot['right_idx'] = right_idx

            if left_idx < 0 and right_idx > part._length:
                dots_data.pop(0)
                if len(dots_data) == 0:
                    start_idx = self.get_start_idx(part)
                    dots_data.append({'left_idx': start_idx, 'right_idx': start_idx})

            if left_idx >= 0:
                part.set_led_color(left_idx,  (255,255,255))
            if right_idx < part._length:
                part.set_led_color(right_idx, (255,255,255))



class SwipeLeftRight(Animation):
    RESET_RGB = (0,0,0)
    NB_CYCLES_PER_ANIMATION = 1

    def __init__(self, rainbow, speed, duration):
        super(self.__class__, self).__init__(rainbow, speed, duration)
        self._cnst_angular_speed = random.choice([False, True])
        self._synchronize_parts = random.choice([False, True])

        if self._synchronize_parts:
            self._ref_part = [part for part in self.get_parts() if part._length == self.MAX_PART_LEN][0]
            self.initialize_part_data(self._ref_part)
        else:
            [self.initialize_part_data(part) for part in self.get_parts()]


    def initialize_part_data(self, part):
        part_data = self.get_data(part)
        part_data['left_idx'] = int(random.uniform(.2, .4)*part._length)
        part_data['left_is_opening'] = True
        part_data['right_idx'] = int(random.uniform(.6, .8)*part._length)
        part_data['right_is_opening'] = True


    def run_period(self, part, period_cnt):
        def sign(boolean):
            return 1 if boolean else -1

        if self._synchronize_parts:
            part_data = self.get_data(self._ref_part)
        else:
            part_data = self.get_data(part)


        if not self._synchronize_parts or part._id == self._ref_part._id:
            left_idx  = part_data['left_idx']  - sign(part_data['left_is_opening'])
            right_idx = part_data['right_idx'] + sign(part_data['right_is_opening'])

            if left_idx == -1 and part_data['left_is_opening']:
                left_idx = int(random.uniform(0., -.2)*part._length)
                part_data['left_is_opening'] = False
            
            if right_idx == part._length and part_data['right_is_opening']:
                right_idx = int(random.uniform(1., 1.2)*part._length)
                part_data['right_is_opening'] = False

            if right_idx - left_idx <= 5:
                part_data['left_is_opening'] = True
                part_data['right_is_opening'] = True

            part_data['left_idx'] = left_idx
            part_data['right_idx'] = right_idx

        else:
            left_idx  = int(part_data['left_idx'] * part._length / self._ref_part._length)
            right_idx = int(part_data['right_idx'] * part._length / self.MAX_PART_LEN)


        part.set_uniform_color()

        [part.set_led_color(idx, (0,0,0)) for idx in range(0, left_idx+1)]
        [part.set_led_color(idx, (0,0,0)) for idx in range(right_idx, part._length)]

        
        


class SwipeUpDown(Animation):
    RESET_RGB = (0,0,0)
    NB_CYCLES_PER_ANIMATION = 1

    def __init__(self, rainbow, speed, duration):
        super(self.__class__, self).__init__(rainbow, speed, duration)
        self._modulus = self._modulus = random.randint(2,self.NB_RAINBOW_PARTS)
        self._direction = random.choice([-1, 1])
        self._factor_multiplier = random.choice([0.3, 1, 1000])
        self._cnst_angular_speed = False

    def scale_rgb_brightness(self, rgb, factor):
        return tuple(min(int(1.0*c/factor), 255) for c in rgb)

    def run_step(self, part, step_cnt):
        period_cnt = int(self.get_period_cnt(part, step_cnt))
        factor = (period_cnt + self._direction*part._id + self.NB_RAINBOW_PARTS) % self._modulus
        factor =  1 + factor * self._factor_multiplier
        scaled_rgb = self.scale_rgb_brightness(part._base_rgb, factor)
        part.set_uniform_color(scaled_rgb)
        

class Gradients(Animation):
    RESET_RGB = (0,0,0)
    NB_CYCLES_PER_ANIMATION = 2
 

    def __init__(self, rainbow, speed, duration):
        super(self.__class__, self).__init__(rainbow, speed, duration)
        self._direction = random.choice([-1, 1])
        self._cnst_angular_speed = random.choice([True, True, False])

        palette_name = random.choice(self.COLOR_PALETTES.keys())
        print palette_name
        palette = self.COLOR_PALETTES[palette_name]
        if random.random() < 0.25: # we dicretice
            nb_colors = random.randint(3, 5)
            discretize_step = int(math.ceil(1.*len(palette)/(nb_colors)))
            palette = palette[1::discretize_step] #*nb_colors*3
            if random.random() < 0.25: # we noisify
                palette *= int(self.MAX_PART_LEN/nb_colors)

        self._color_palette = palette


    def run_step(self, part, step_cnt):
        palette_len = len(self._color_palette)
        def palette_idx(led_idx):
            period_cnt = self.get_period_cnt(part, step_cnt)
            moving_idx = period_cnt + self._direction*led_idx + part._length # We add the length again to ensure positivity  
            return int(round(moving_idx*palette_len/part._length)) % palette_len
        
        leds_rgb = [self._color_palette[palette_idx(led_idx)] for led_idx in range(part._length)]
        part.set_leds_rgb(leds_rgb)


class Pendulum(Animation):
    RESET_RGB = (0,0,0)
    NB_CYCLES_PER_ANIMATION = 2
    GRAVITY = 10

    def __init__(self, rainbow, speed, duration):
        super(self.__class__, self).__init__(rainbow, speed, duration)
        self._pendel_base_length = random.uniform(5, 20) 
        self._pendel_delta_pct = random.uniform(.03, .10)
        self._pendel_delta_direction = random.choice([-1, +1, +1])

        [self.initialize_part_data(part) for part in self.get_parts()]


    def initialize_part_data(self, part):
        part_data = self.get_data(part)
        radius = self._pendel_base_length + \
            self._pendel_delta_direction*self._pendel_base_length*self._pendel_delta_pct*(part._id-int(self.NB_RAINBOW_PARTS/2))
        part_data['omega'] = math.sqrt(1.*radius/self.GRAVITY)



    def run_period(self, part, period_cnt):
        part.set_uniform_color()
        part_data = self.get_data(part)

        time_s = 1.*period_cnt*self.SPEED_MS/1000
        angle = math.cos(part_data['omega']*time_s) # [-1, 1]
        pct = (angle+1)/2
        dot_idx_1 = int(round((part._length-1) * pct))
        dot_idx_2 = int(round((part._length-1) * (1-pct)))

        part.set_led_color(dot_idx_1,  (255,255,255))
        part.set_led_color(dot_idx_2,  (255,255,255))


