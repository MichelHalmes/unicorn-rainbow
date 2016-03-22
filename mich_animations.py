import random

from _base_classes import Animation


class Colorwipe(Animation):
    RESET_RGB = (0,0,0)
    NB_CYCLES_PER_ANIMATION = 4

    def run_step(self, part, step_cnt):
        pixel_idx = int(step_cnt * part._length / self.NORMAL_NB_STEPS_PER_CYCLE) % part._length
        if pixel_idx == 0:
            part.set_uniform_color((0,0,0))

        part.set_pixel_color(pixel_idx)

class Flashparts(Animation):
    RESET_RGB = (0,0,0)
    NB_CYCLES_PER_ANIMATION = 3

    def run_step(self, part, step_cnt):
        if step_cnt % self.NORMAL_NB_STEPS_PER_STABLE_PERIOD != 0:
            return

        periods = step_cnt/self.NORMAL_NB_STEPS_PER_STABLE_PERIOD

        if (periods+part._part_idx) % 2 == 0:
            part.set_uniform_color()
        else:
            part.set_uniform_color((0,0,0))

class Gradients(Animation):
    RESET_RGB = (0,0,0)
    NB_CYCLES_PER_ANIMATION = 3

    def run_step(self, part, step_cnt):
        RAINBOW_LEN = len(self.RAINBOW_RGB)
        start_idx = 0 # step_cnt % RAINBOW_LEN
        leds_rgb = [self.RAINBOW_RGB[int(start_idx + (led_idx*RAINBOW_LEN/part._length))%RAINBOW_LEN] for led_idx in range(part._length)]
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
