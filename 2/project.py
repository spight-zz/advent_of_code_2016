import sys


class BathroomCoder(object):
    DIRS = {
        'U': (0, -1),
        'D': (0, 1),
        'R': (1, 0),
        'L': (-1, 0),
    }

    def __init__(self, matrix, x, y):
        self.matrix = matrix
        self.x = x
        self.y = y

    def move(self, direction):
        instruction = self.DIRS[direction]

        self.x += instruction[1]
        self.y += instruction[0]

        if self.is_valid():
            return True
        else:
            self.x -= instruction[1]
            self.y -= instruction[0]
            return False

    def is_valid(self):
        if self.x < 0 or self.y < 0:
            return False

        try:
            if self.current is None:
                return False
        except IndexError:
            return False

        return True

    @property
    def current(self):
        return self.matrix[self.x][self.y]

    def run(self, lines):
        output = ""
        for line in lines:
            line = line.strip()
            for char in line:
                self.move(char)

            output += str(self.current)
        return output

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    keypad = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]

    print "Part 1:", BathroomCoder(keypad, 1, 1).run(lines)

    keypad = [
        [None, None, 1,   None, None],
        [None, 2,    3,   4,    None],
        [5,    6,    7,   8,    9],
        [None, 'A',  'B', 'C',  None],
        [None, None, 'D', None, None],
    ]

    print "Part 2:", BathroomCoder(keypad, 2, 2).run(lines)
