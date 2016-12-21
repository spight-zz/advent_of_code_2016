import sys


class DirectionHelper(object):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    DIRECTIONS = ['North', 'East', 'South', 'West']

    def __init__(self):
        self.dir = self.NORTH

    def right(self):
        self.dir = (self.dir + 1) % 4
        return self.dir

    def left(self):
        self.dir = (self.dir + 3) % 4  # To avoid negative modulo, add 4-1
        return self.dir

    def next(self, instruction):
        if instruction == 'R':
            return self.right()
        elif instruction == 'L':
            return self.left()
        else:
            raise ValueError("Instruction must be either 'R' or 'L'")

    def pretty(self, code):
        return self.DIRECTIONS[code]


class Walker(object):
    def __init__(self, instructions):
        self.instructions = instructions
        self.last = (0, 0)
        self.loci = []

    def run(self):
        movements = [0, 0, 0, 0]  # North, East, South, West
        helper = DirectionHelper()

        for instruction in self.instructions:
            direction = helper.next(instruction[0])
            instruct = (direction, int(instruction[1:]))
            if self.moveto_and_check(movements, instruct):
                break

        print(movements[0] + movements[1] - movements[2] - movements[3])

    def moveto_and_check(self, movements, instruction):
        for i in range(instruction[1]):
            movements[instruction[0]] += 1
            if self.visit_and_check(movements):
                return self.last

        return False

    def visit_and_check(self, movement):
        north = movement[0] - movement[2]
        east = movement[1] - movement[3]
        self.last = (north, east)
        if self.last in self.loci:
            return True
        else:
            self.loci.append(self.last)
            return False


def convert_instructions(input):
    return input.split(", ")


if __name__ == '__main__':
    Walker(convert_instructions(sys.stdin.read())).run()
