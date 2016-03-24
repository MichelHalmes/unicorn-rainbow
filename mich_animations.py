import random

from _base_classes import Animation


class SwipeLeftRight(Animation):
    RESET_RGB = (0,0,0)
    NB_CYCLES_PER_ANIMATION = 3

    def __init__(self, rainbow, speed, duration):
        super(self.__class__, self).__init__(rainbow, speed, duration)
        self._cnst_angular_speed = True #random.choice([False, False, True])
        self._synchronize_parts = True

        if self._synchronize_parts:
            self._ref_part = [part for part in self.get_parts() if part._length == self.MAX_PART_LEN][0]
            self.initialize_part_data(self._ref_part)
        else:
            [self.initialize_part_data(part) for part in self.get_parts()]


    def initialize_part_data(self, part):
        part_data = self.get_data(part)
        part_data['left_idx'] = int(0.3*part._length)
        part_data['left_is_opening'] = True
        part_data['right_idx'] = int(0.7*part._length)
        part_data['right_is_opening'] = True


    def run_period(self, part, period_cnt):
        def sign(boolean):
            return 1 if boolean else -1

        if self._synchronize_parts:
            part_data = self.get_data(self._ref_part)
        else:
            part_data = self.get_data(part)


        if not self._synchronize_parts or part._part_idx == self._ref_part._part_idx:
            left_idx  = part_data['left_idx']  - sign(part_data['left_is_opening'])
            right_idx = part_data['right_idx'] + sign(part_data['right_is_opening'])

            if left_idx == -1 and part_data['left_is_opening']:
                left_idx = 0
                part_data['left_is_opening'] = False
            
            if right_idx == part._length and part_data['right_is_opening']:
                right_idx = part._length
                part_data['right_is_opening'] = False

            if left_idx >= right_idx:
                part_data['left_is_opening'] = True
                part_data['right_is_opening'] = True

            part_data['left_idx'] = left_idx
            part_data['right_idx'] = right_idx

        else:
            left_idx  = int(1.*part_data['left_idx'] * part._length / self._ref_part._length)
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
        self._factor_multiplier = 1000 #random.choice([0.3, 1, 1000])
        self._cnst_angular_speed = False

    def run_step(self, part, step_cnt):
        period_cnt = int(self.get_period_cnt(part, step_cnt))
        factor = (period_cnt + self._direction*part._part_idx + self.NB_RAINBOW_PARTS) % self._modulus
        factor =  1 + factor * self._factor_multiplier
        scaled_rgb = self.scale_rgb_brightness(part._base_rgb, factor)
        part.set_uniform_color(scaled_rgb)
        

class Gradients(Animation):
    RESET_RGB = (0,0,0)
    NB_CYCLES_PER_ANIMATION = 3

    def __init__(self, rainbow, speed, duration):
        super(self.__class__, self).__init__(rainbow, speed, duration)
        self._direction = random.choice([-1, 1])
        self._cnst_angular_speed = random.choice([True, True, False])


    def run_step(self, part, step_cnt):
        RAINBOW_LEN = len(self.RAINBOW_RGB)
        def rainbow_idx(led_idx):
            period_cnt = self.get_period_cnt(part, step_cnt)
            moving_idx = period_cnt + self._direction*led_idx + part._length # We add the length again to ensure positivity  
            return int(moving_idx*RAINBOW_LEN/part._length) % RAINBOW_LEN
        
        leds_rgb = [self.RAINBOW_RGB[rainbow_idx(led_idx)] for led_idx in range(part._length)]
        part.set_leds_rgb(leds_rgb)

class Commet(Animation):
    RESET_RGB = None
    NB_CYCLES_PER_ANIMATION = 3

    def run_step(self, part, step_cnt):
        if step_cnt % self.NORMAL_NB_STEPS_PER_STABLE_PERIOD != 0:
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
