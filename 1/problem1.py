

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
        self.loci = []

    def run(self):
        movements = [0, 0, 0, 0]  # North, East, South, West
        helper = DirectionHelper()

        for instruction in self.instructions:
            direction = helper.next(instruction[0])
            movements[direction] += int(instruction[1:])

        print_it(movements, helper)

def print_it(movements, helper):
    north = movements[helper.NORTH] - movements[helper.SOUTH]
    east = movements[helper.EAST] - movements[helper.WEST]
    print("(%s by %s)"%(north, east))


def convert_instructions(input):
    return input.split(", ")



if __name__ == '__main__':
    inst = convert_instructions("R2, L3, R2, R4, L2, L1, R2, R4, R1, L4, L5, R5, R5, R2, R2, R1, L2, L3, L2, L1, R3, L5, R187, R1, R4, L1, R5, L3, L4, R50, L4, R2, R70, L3, L2, R4, R3, R194, L3, L4, L4, L3, L4, R4, R5, L1, L5, L4, R1, L2, R4, L5, L3, R4, L5, L5, R5, R3, R5, L2, L4, R4, L1, R3, R1, L1, L2, R2, R2, L3, R3, R2, R5, R2, R5, L3, R2, L5, R1, R2, R2, L4, L5, L1, L4, R4, R3, R1, R2, L1, L2, R4, R5, L2, R3, L4, L5, L5, L4, R4, L2, R1, R1, L2, L3, L2, R2, L4, R3, R2, L1, L3, L2, L4, L4, R2, L3, L3, R2, L4, L3, R4, R3, L2, L1, L4, R4, R2, L4, L4, L5, L1, R2, L5, L2, L3, R2, L2")
    # inst = convert_instructions("R5, L5, R5, R3")
    Walker(inst).run()
