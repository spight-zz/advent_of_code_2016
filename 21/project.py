import sys
from functools import partial
import string


class Machine(object):
    def __init__(self, register):
        self._register = list(register)
        self.instructions = []
        self.current = 0
        self._rotate_reverse = None

    @property
    def register(self):
        return ''.join(self._register)

    @property
    def _rotate_reverse_lookup(self):
        if self._rotate_reverse is None:
            table = {}
            test_str = string.printable[0:len(self.register)]

            for initial_idx, char in enumerate(test_str):
                self._get_based_offset(test)
                table[test_str.index(char)] = initial_idx

            self._rotate_reverse = table

        return self._rotate_reverse

    def process_cmd(self, cmd, undo=False):
        parts = cmd.split()
        if hasattr(self, parts[0]):
            return getattr(self, parts[0])(*parts[1:], undo=undo)

    def swap(self, *args, **kwargs):
        if args[0] == 'position':
            x = int(args[1])
            y = int(args[4])
            tmp_ = self._register[x]
            self._register[x] = self._register[y]
            self._register[y] = tmp_
        elif args[0] == 'letter':
            tmp_dict = {args[1]: args[4], args[4]: args[1]}
            self._register = map(lambda x: tmp_dict.get(x, x), self.register)

        return True

    def reverse(self, *args, **kwargs):
        i = int(args[1])
        j = int(args[3])
        self._register = self._register[0:i] + \
            list(reversed(self._register[i:j + 1])) + \
            self._register[j + 1:]

    def move(self, *args, **kwargs):
        i = int(args[1])
        j = int(args[4])

        if kwargs.pop('undo', False):
            i, j = j, i

        tmp_ = self._register.pop(i)
        self._register.insert(j, tmp_)

    def _get_based_offset(self, line, char):
        offset = line.index(char) + 1
        if offset > 4:
            offset += 1
        return offset

    def rotate(self, *args, **kwargs):
        undo = kwargs.pop('undo', False)

        if args[0] == 'based':
            idx = self.register.index(args[5])

            if undo:
                if len(self.register) != 8:
                    raise ValueError("Register must be length 8 for undo")

                if idx % 2 == 1:
                    offset = 7 - idx / 2
                else:
                    offset = (2 - ((idx + 7) % 8) / 2) % 8

            else:
                offset = idx + 1
                if idx >= 4:
                    offset += 1

            return self._rotate('right', offset)

        else:
            offset = int(args[1])
            return self._rotate(args[0], offset, undo=undo)

    def _rotate(self, direction, offset, undo=False):
        if undo:
            direction = {'right': 'left', 'left': 'right'}[direction]

        if direction == 'right':
            func = self._register.insert
            func = partial(func, 0)
            popper = -1
        else:
            func = self._register.append
            popper = 0

        for i in range(offset):
            func(self._register.pop(popper))


class Project(object):
    def __init__(self, fh):
        self.input = fh

    def run1(self, ):
        machine = Machine('abcdefgh')

        for line in self.input:
            machine.process_cmd(line)
        return machine.register

    def run2(self,):
        machine = Machine('fbgdceah')
        for line in reversed(self.input.readlines()):
            machine.process_cmd(line, True)

        return machine.register


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        p = Project(f)
        print "Part 1:", p.run1()
        f.seek(0)
        print "Part 2:", p.run2()
