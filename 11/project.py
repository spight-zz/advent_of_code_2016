import sys
from itertools import combinations
from Queue import Queue


class RTGFry(Exception):
    pass


class State(object):
    def __init__(self, num_floors=2, distance=None, parent=None):
        self.floors = [set() for _ in range(num_floors)]
        self.elevator = 1
        self.distance = distance  # distance from root
        self.parent = parent  # None makes this the root

    @property
    def current_floor(self):
        return self.floors[self.elevator - 1]

    def serialize(self):
        output = []
        pair_num = 0
        pair_map = {}
        for floor in self.floors:
            devices = []
            for device in floor:
                if device.element not in pair_map:
                    pair_map[device.element] = pair_num
                    pair_num += 1

                devices.append(str(pair_map[device.element]) + device.type)

            output.append(sorted(devices))

        return str(output) + ":elevator=" + str(self.elevator)

    def clone(self):
        other = State(0)
        other.elevator = self.elevator
        for floor in self.floors:
            other.floors.append(set(floor))
        return other

    def add(self, item, floor=None):
        if floor is None:
            add_to = self.current_floor
        else:
            add_to = self.floors[floor-1]
        add_to.add(item)

    @property
    def lowest_populated_floor(self):
        for i, floor in enumerate(self.floors):
            if len(floor) != 0:
                return i + 1

    def itermoves(self):
        if self.elevator == self.lowest_populated_floor:
            directions = ['up']
        elif self.elevator == len(self.floors):
            directions = ['down']
        else:
            directions = ['up', 'down']

        num_objects = 2

        if len(self.current_floor) < num_objects:
            num_objects = len(self.current_floor)

        while num_objects > 0:
            for pair in combinations(self.current_floor, num_objects):
                for direction in directions:
                    yield direction, pair
            num_objects -= 1

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
            self.add(pair[0])
        if len(pair) == 2:
            self.add(pair[1])

    def is_complete(self, ):
        for i, floor in enumerate(self.floors):
            if len(floor) > 0 and i != len(self.floors) - 1:
                return False
        return True

    def is_valid(self, ):
        for floor in self.floors:
            if not any_rtg(floor):
                continue
            for item in floor:
                if item.type == 'chip' and \
                        not any_match(floor, 'rtg', item.element):
                    return False
        return True

    def __str__(self):
        output = []
        for i, floor in enumerate(self.floors):
            if self.elevator == i+1:
                marker = "*"
            else:
                marker = " "

            output.append("%s#%d: floor: %s\n" % (marker, i+1, sorted(floor)))

        return "".join(reversed(output))


class Item(object):
    def __init__(self, element):
        self.element = element
        self.type = None

    def __repr__(self):
        # return '<%s: %s>' % (self.type, self.element)
        if self.type == 'rtg':
            short_type = 'G'
        else:
            short_type = 'M'
        return '%s%s' % (self.element, short_type)


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

    def run_test(self, ):
        root = State(4, distance=0)
        lg = RTG("L")
        lm = Chip("L")
        hg = RTG("H")
        hm = Chip("H")
        root.add(lm, 1)
        root.add(hm, 1)
        root.add(hg, 2)
        root.add(lg, 3)

        result = find_nearest_correct(root)
        print(result)
        print(result.distance)

    def run1(self):
        p = State(4, distance=0)
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

        result = find_nearest_correct(p)
        print(result)
        print(result.distance)

    def run2(self):
        p = State(4, distance=0)
        p.add(RTG("strontium"), 1)
        p.add(Chip("strontium"), 1)
        p.add(RTG("plutonium"), 1)
        p.add(Chip("plutonium"), 1)
        p.add(Chip("elerium"), 1)
        p.add(RTG("elerium"), 1)
        p.add(Chip("dilithium"), 1)
        p.add(RTG("dilithium"), 1)
        p.add(RTG("thulium"), 2)
        p.add(RTG("ruthenium"), 2)
        p.add(Chip("ruthenium"), 2)
        p.add(RTG("curium"), 2)
        p.add(Chip("curium"), 2)
        p.add(Chip("thulium"), 3)

        result = find_nearest_correct(p)
        print(result)
        print(result.distance)


def any_rtg(iterable):
    return _any(iterable, lambda x: x.type == 'rtg')


def any_match(iterable, type_, element):
    return _any(iterable, lambda x: x.type == type_ and x.element == element)


def _any(iterable, func):
    for element in iterable:
        if func(element):
            return True
    return False


def find_nearest_correct(root, max_distance=1000):
    queue = Queue()
    seen = {}
    queue.put(root)

    last_distance = 0
    while not queue.empty():
        state = queue.get()
        if state.distance > last_distance:
            last_distance = state.distance
            print(last_distance)
        sys.stdout.flush()
        if state.distance > max_distance:
            return False

        if state.is_complete():
            return state

        if state.is_valid():
            for move in state.itermoves():
                new_state = state.clone()
                new_state.move(*move)
                new_state.parent = state
                new_state.distance = state.distance + 1

                if new_state.is_valid():
                    if new_state.serialize() not in seen:
                        seen[new_state.serialize()] = new_state
                        queue.put(new_state)


if __name__ == '__main__':
    Project().run1()
    Project().run2()
