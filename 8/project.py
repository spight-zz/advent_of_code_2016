import sys
import re
import json

class Project(object):
    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.init_diagram(width, height)

    def init_diagram(self, width, height):
        self.diagram = [[ '.' for __ in range(width) ] for _ in range(height)]

    def run(self, ):
        for line in sys.stdin:

            instruction = self.get_line(line)
            instruction[0](self, *instruction[1:])


        total = 0
        for row in self.diagram:
            for column in row:
                if column is '#':
                    total += 1
        print total

    def get_line(self, line):
        match = re.match(r'rect +(\d+)x(\d+)', line)
        if match:
            return (Project.rect, int(match.group(1)), int(match.group(2)))

        match = re.match(r'rotate (column|row) (x|y)=(\d+) by (\d+)', line)
        if match:
            if match.group(1) == 'column':
                func = Project.rotate_column
            else:
                func = Project.rotate_row

            return (func, int(match.group(3)), int(match.group(4)))

        raise ValueError("Unexpected line: '%s'" % line )

    def rotate_column(self, column, by):
        new = [[] for _ in range(self.height)]
        for i in range(self.height):
            new[(i + by) % self.height] = self.diagram[i][column]

        for i, elem in enumerate(new):
            self.diagram[i][column] = elem


    def rotate_row(self, row, by):
        new = [[] for _ in range(self.width)]
        for i, elem in enumerate(self.diagram[row]):
            new[(i+by) % self.width] = elem
        self.diagram[row] = new

    def rect(self, x, y):
        for dx in range(x):
            for dy in range(y):
                try:
                    self.diagram[dy][dx] = '#'
                except IndexError:
                    pass


def print_array(array):
    for ary in array:
        for elem in ary:
            sys.stdout.write(str(elem))
        sys.stdout.write("\n")


if __name__ == '__main__':
    try:
        p = Project(6, 50)
        p.run()
    finally:
        print_array(p.diagram)
