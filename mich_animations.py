import random

from _base_classes import Animation


class Colorwipe(Animation):
    RESET_RGB = (0,0,0)
    NB_CYCLES_PER_ANIMATION = 3

    def run_step(self, part, step_cnt):
        pixel_idx = int(step_cnt * part._length / self.NORMAL_NB_STEPS_PER_CYCLE) % part._length
        if pixel_idx == 0:
            part.set_uniform_color((0,0,0))

        part.set_pixel_color(pixel_idx)



class Flashparts(Animation):
    RESET_RGB = (0,0,0)
    NB_CYCLES_PER_ANIMATION = 1

    def __init__(self, speed, duration):
        super(self.__class__, self).__init__(speed, duration)
        self._modulus = self._modulus = random.randint(2,self.NB_RAINBOW_PARTS)
        self._direction = random.choice([-1, 1])
        self._factor_multiplier = random.choice([0.3, 1, 1000])

    def run_step(self, part, step_cnt):
        period_cnt = step_cnt/self.NORMAL_NB_STEPS_PER_STABLE_PERIOD
        factor = (self.NB_RAINBOW_PARTS + period_cnt + self._direction*part._part_idx) % self._modulus
        factor =  1 + factor * self._factor_multiplier
        scaled_rgb = self.scale_rgb_brightness(part._base_rgb, factor)
        part.set_uniform_color(scaled_rgb)
        

class Gradients(Animation):
    RESET_RGB = (0,0,0)
    NB_CYCLES_PER_ANIMATION = 3

    def __init__(self, speed, duration):
        super(self.__class__, self).__init__(speed, duration)
        self._direction = random.choice([-1, 1])
        self._cnst_angular_speed = random.choice([True, True, False])


    def run_step(self, part, step_cnt):
        RAINBOW_LEN = len(self.RAINBOW_RGB)
        def rainbow_idx(led_idx):
            moving_idx = self.get_moving_idx(led_idx, step_cnt, part, self._direction,self._cnst_angular_speed)
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