import sys


class Trapway(object):
    def __init__(self, width=5):
        self.seen = {}
        self.width = width

    def find_traps(self, previous):
        if previous in self.seen:
            return self.seen[previous]

        traps = [False for _ in range(self.width)]
        for i in range(self.width):
            if i == 0:
                l = False
                c, r = previous[0], previous[1]
            elif i == self.width - 1:
                r = False
                l, c = previous[-2], previous[-1]
            else:
                l, c, r = previous[i - 1:i + 2]
            traps[i] = self.is_trap(l, c, r)

        traps = tuple(traps)
        self.seen[previous] = traps
        return traps

    def is_trap(self, left, center, right):
        """each of left, center, and right is a boolean. True for trap"""
        return left and not right or right and not left

    def print_row(self, row):
        for space in row:
            if space:
                sys.stdout.write("^")
            else:
                sys.stdout.write(".")
        print


class Project(object):
    def __init__(self, fh):
        self.input = fh

    def parse_row(self, line):
        return tuple(map(lambda x: x == '^', line))

    def run(self, target_rows):
        initial = self.input.read().strip()
        previous = self.parse_row(initial)
        traps = Trapway(len(previous))

        safe_tiles = previous.count(False)
        rows = 1

        while rows < target_rows:
            new = traps.find_traps(previous)
            previous = new

            safe_tiles += previous.count(False)
            rows += 1

        return safe_tiles


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        p = Project(f)
        print "Part 1:", p.run(40)
        f.seek(0)
        print "Part 2:", p.run(400000)
