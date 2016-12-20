import sys
import itertools

class RTGFry(Exception):
    pass

class State(object):
    def __init__(self, num_floors=2):
        self.floors = [set() for _ in range(num_floors)]
        self.elevator = 1

    @property
    def current_floor(self):
        return self.floors[self.elevator - 1]

    def clone(self):
        other = State(0)
        other.elevator = self.elevator
        for floor in self.floors:
            other.floors.append(set(floor))
        return other

    def add(self, item, floor):
        self.floors[floor-1].add(item)

    def itermoves(self):
        if self.elevator == 1:
            directions = ['up']
        elif self.elevator == len(self.floors):
            directions = ['down']
        else:
            directions = ['up', 'down']

        if len(self.current_floor) < 2:
            for direction in directions:
                yield direction, pair

        for pair in itertools.combinations(self.current_floor, 2):
            for direction in directions:
                yield direction, pair

    def move(self, direction, pair):
        if pair:
            self.current_floor.remove(pair[0])
        if len(pair) == 2:
            self.current_floor.remove(pair[1])

        if direction == 'up':
            self.elevator += 1
        else:
            self.elevator -= 1

        if pair:
            self.current_floor.add(pair[0])
        if len(pair) == 2:
            self.current_floor.add(pair[1])


    def is_complete(self, ):
        for i, floor in enumerate(self.floors):
            if len(floor) > 0 and i != len(self.floors) - 1:
                return False
        return True

    def is_valid(self, ):
        for floor in self.floors:
            if not any_rtg(floor):
                print("skipping - no generator")
                continue
            for item in floor:
                if item.type == 'chip' and \
                    not any_match(floor, 'rtg', item.element):
                    return False
        return True


class Item(object):
    def __init__(self, element):
        self.element = element
        self.type = None

    def __repr__(self):
        return '<%s: %s>' % (self.type, self.element)

class Chip(Item):
    def __init__(self, element):
        self.element = element
        self.type = 'chip'

class RTG(Item):
    def __init__(self, element):
        self.element = element
        self.type = 'rtg'

class Project(object):
    def __init__(self, ):
        pass

    def run(self, ):
        for line in sys.stdin:
            pass


def any_rtg(iterable):
    return _any(iterable, lambda x: x.type == 'rtg')

def any_match(iterable, type_, element):
    return _any(iterable, lambda x: x.type == type_ and x.element == element)

def _any(iterable, func):
    for element in iterable:
        if func(element):
            return True
    return False



def find_depth(state, depth=0, max_depth=1):
    print(depth, max_depth)
    if depth >= max_depth:
        return False
    for move in state.itermoves():
        temp_state = state.clone()
        temp_state.move(*move)
        if temp_state.is_complete():
            return depth
        elif temp_state.is_valid():
            tmp_depth = find_depth(temp_state,
                               depth=depth,
                               max_depth=max_depth - 1)
            if tmp_depth:
                return tmp_depth + 1
    return False


if __name__ == '__main__':
    p = State(4)
    # p.add(RTG("strontium"), 1)
    # p.add(Chip("strontium"), 1)
    # p.elevator = 1

    p.add(RTG("strontium"), 1)
    p.add(Chip("strontium"), 1)
    p.add(RTG("plutonium"), 1)
    p.add(Chip("plutonium"), 1)
    p.add(RTG("thulium"), 2)
    p.add(RTG("ruthenium"), 2)
    p.add(Chip("ruthenium"), 2)
    p.add(RTG("curium"), 2)
    p.add(Chip("curium"), 2)
    p.add(Chip("thulium"), 3)

    print find_depth(p, max_depth=8)

    # for move in p.itermoves():
    #     print move
    # print p.is_valid()
