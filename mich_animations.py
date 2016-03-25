import random
import math

from _base_classes import Animation

class Snake(Animation):
    RESET_RGB = None
    NB_CYCLES_PER_ANIMATION = 2
    DOT_RELATIVE_SPEED = 4
    BLINK_PERIODS = 10

    def __init__(self, rainbow, speed, duration):
        super(self.__class__, self).__init__(rainbow, speed, duration)
        
        [self.initialize_part_data(part) for part in self.get_parts()]

        self.get_data()['snake'] = {
            'length': 4,
            'head': {'part_id': 2, 'idx': 5, 'direction': 1 },
            'tail': {}
        }


    def initialize_part_data(self, part):
        part_data = self.get_data(part)
        part_data['dots'] = []

        dot = self.get_new_dot(part)
        self.get_data(part)['dots'].append(dot)

    def get_new_dot(self, part):
        start_idx = random.randint(int(0.25*part._length), int(0.75*part._length))
        return {'idx': start_idx, 'direction': random.choice([-1, 1]), 'blink_cnt': 2}

    def find_dot_at_idx(self, part, idx):
        res = [d for d in self.get_data(part)['dots'] if int(d['idx']) == idx]
        assert len(res)<2
        return res[0] if res else None


    def run_parts_period(self, step_cnt):
        for part in self.get_parts():
            part.set_uniform_color()
        self.run_snake_period()
        super(self.__class__, self).run_parts_period(step_cnt)

    def run_snake_period(self):
        def get_distance_to_edge(part, led_idx, direction):
            return part._length-1 - led_idx if direction == 1 else led_idx


        length = self.get_data()['snake']['length']
        head_data = self.get_data()['snake']['head']
        tail_data = self.get_data()['snake']['tail']

        # HEAD
        head_part = self.get_parts()[head_data['part_id']]
        head_direction = head_data['direction']
        head_idx = head_data['idx'] = head_data['idx'] + head_data['direction']

        if get_distance_to_edge(head_part, head_idx, head_direction) == -1:
            tail_data['part_id'] = head_part._id
            tail_data['direction'] = head_direction
            tail_data['idx'] = (0 if head_idx == -1 else head_part._length -1)

            head_data['part_id'] = (head_part._id + random.choice([-1, 1])) % self.NB_RAINBOW_PARTS
            head_part = self.get_parts()[head_data['part_id']]
            head_direction = head_data['direction'] = (1  if head_idx == -1 else -1)
            head_idx = head_data['idx'] = (0 if head_idx == -1 else head_part._length -1)

        head_length = min(length, 1 + get_distance_to_edge(head_part, head_idx, -head_direction))
        
        for led_idx in range(head_idx, head_idx - head_length*head_direction, -head_direction):
            head_part.set_led_color(led_idx, (5, 5, 5))

        # HANDLE DOT AT START
        start_dot = self.find_dot_at_idx(head_part, head_idx)
        if start_dot:
            start_dot['blink_cnt'] = 2 * length

        # TAIL
        tail_length = length - head_length

        if tail_length == 0:
            end_idx = head_idx - head_direction*head_length
            end_part = head_part
            
        else:
            tail_part = self.get_parts()[tail_data['part_id']]
            tail_direction = tail_data['direction']
            tail_idx = tail_data['idx']
            for led_idx in range(tail_idx, tail_idx - tail_length*tail_direction, -tail_direction):
                tail_part.set_led_color(led_idx, (5, 5, 5))

            end_idx = tail_idx - tail_direction*tail_length
            end_part = tail_part


        # HANDLE DOT AT END
        end_dot = self.find_dot_at_idx(end_part, end_idx)
        if end_dot:
            self.get_data()['snake']['length'] += 1
            self.get_data(end_part)['dots'].remove(end_dot)

        



    def run_period(self, part, period_cnt):
        dots_data = self.get_data(part)['dots']

        if random.random() < 0.05*part._length/self.MAX_PART_LEN:
            dot = self.get_new_dot(part)
            if not self.find_dot_at_idx(part, dot['idx']):
                dots_data.append(dot)

        for dot in dots_data:

            if dot['blink_cnt'] > 0:
                dot['blink_cnt'] -= 1
            
            else:
                dot_idx = dot['idx'] + 1.*dot['direction'] / self.DOT_RELATIVE_SPEED
                if dot_idx <= 0 or dot_idx >= part._length:
                    dots_data.remove(dot)
                    continue

                if self.find_dot_at_idx(part, math.floor(dot['idx'] + dot['direction'])):
                    dot['blink_cnt'] = self.BLINK_PERIODS
                    dot['direction'] *= -1
                else:
                    dot['idx'] = dot_idx
                    

            if dot['blink_cnt'] % 2 == 1:
                part.set_led_color(int(dot['idx']),  (10, 10, 10))
            else:
                part.set_led_color(int(dot['idx']),  (255, 255, 255))

    

       




class Feynman(Animation):
    RESET_RGB = None
    NB_CYCLES_PER_ANIMATION = 2

    def __init__(self, rainbow, speed, duration):
        super(self.__class__, self).__init__(rainbow, speed, duration)
        
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

    def run_period(self, part, period_cnt):
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
    NB_CYCLES_PER_ANIMATION = 2

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


    def run_step(self, part, step_cnt):
        RAINBOW_LEN = len(self.RAINBOW_RGB)
        def rainbow_idx(led_idx):
            period_cnt = self.get_period_cnt(part, step_cnt)
            moving_idx = period_cnt + self._direction*led_idx + part._length # We add the length again to ensure positivity  
            return int(moving_idx*RAINBOW_LEN/part._length) % RAINBOW_LEN
        
        leds_rgb = [self.RAINBOW_RGB[rainbow_idx(led_idx)] for led_idx in range(part._length)]
        part.set_leds_rgb(leds_rgb)


