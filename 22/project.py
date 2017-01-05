import sys
from itertools import permutations, combinations
import re


class State(object):
    def __init__(self):
        self.data = [[]]
        self.target = None
        self.min_used = 9999999
        self.max_avail = 0

    def expand_to(self, x, y):
        while len(self.data) < x + 1:
            self.data.append([])

        for row in self.data:
            while len(row) < y + 1:
                row.append(None)

    def add(self, x, y, used, size, name):
        self.expand_to(y, x)
        self.data[y][x] = [(name, used), size]

        if used == 0:
            self.max_space = size
        elif used < self.min_used:
            self.min_used = used
        elif size - used > self.max_avail:
            self.max_avail = size - used

    def itermoves(self):
        pass

    def __str__(self):
        output = ""
        for i, row in enumerate(self.data):
            for j, df in enumerate(row):
                if i == 0 and j == 0:
                    def wrapper(x):
                        return "(%s)" % x
                elif i == 0 and j == len(row) - 1:
                    def wrapper(x):
                        return "[%s]" % x
                else:
                    def wrapper(x):
                        return " " * (3 - len(x)) + x + " "

                if df[0][0] == self.target[0][0]:
                    output += wrapper("G")
                else:
                    output += wrapper(str(df[0][1]))

            output += "\n"
        return output

    def lock_target(self):
        self.target = self.data[0][-1]
        print self.target


class Project(object):
    def __init__(self, fh):
        self.input = fh
        self.pos_pattern = re.compile('\/dev\/grid\/node-(x(\d+)-y(\d+))')

    def run1(self, ):
        data = []
        valid = 0

        for i, line in enumerate(self.input):
            # The first two lines are formatting. ignore
            if i < 2:
                continue
            df = self.get_df(line.strip())
            data.append((df[2], df[3]))

        for perm in permutations(data, 2):
            if self.is_valid(perm):
                valid += 1

        return valid

    def run2(self,):
        state = State()
        for i, line in enumerate(self.input):
            if i < 2:
                continue
            df = self.get_df(line.strip())
            state.add(*df)

        state.lock_target()

        print state.target
        print
        print state

    def get_df(self, line):
        parts = line.split()
        match = self.pos_pattern.match(line)
        x = int(match.group(2))
        y = int(match.group(3))
        return x, y, int(parts[2][:-1]), int(parts[1][:-1]), match.group(1)

    def is_valid(self, pair):
        return pair[0][0] > 0 and pair[0][0] <= pair[1][1]


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        p = Project(f)
        # print "Part 1:", p.run1()
        # f.seek(0)
        print "Part 2:", p.run2()
