import random
import math

from _base_classes import Animation

class Snake(Animation):
    RESET_RGB = None
    NB_CYCLES_PER_ANIMATION = 10
    VARIETY = 5

    DOT_RELATIVE_SPEED = 4
    BLINK_PERIODS = 10

    def __init__(self, rainbow):
        super(self.__class__, self).__init__(rainbow)
        
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
            head_part.set_led_color(led_idx, (250, 250, 250))

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
            if tail_length > tail_part._length:
                raise StopIteration()
            tail_direction = tail_data['direction']
            tail_idx = tail_data['idx']
            for led_idx in range(tail_idx, tail_idx - tail_length*tail_direction, -tail_direction):
                tail_part.set_led_color(led_idx, (250, 250, 250))

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
                    

            if dot['blink_cnt'] and (period_cnt % 2 == 0):
                part.set_led_color(int(dot['idx']),  (250, 250, 250))
            else:
                part.set_led_color(int(dot['idx']),  (0, 0, 0))
