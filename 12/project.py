import sys


class Machine(object):
    def __init__(self, verbose):
        self.verbose = verbose
        self.registers = dict(a=0,
                              b=0,
                              c=1,
                              d=0,
                              )
        self.instructions = []
        self.current = 0

    def process_current(self):
        try:
            cmd = self.instructions[self.current]
        except IndexError:
            raise StopIteration()
        output = self._process_cmd(cmd)
        self.current += 1
        return output

    def _process_cmd(self, cmd):
        parts = cmd.split()
        if hasattr(self, parts[0]):
            return getattr(self, parts[0])(*parts[1:])

    def cpy(self, x, y):
        if self.verbose:
            print("CPY", x, y)
        try:
            x = int(x)
        except ValueError:
            x = self.registers[x]

        self.registers[y] = x
        return True

    def inc(self, x):
        if self.verbose:
            print("INC", x)
        self.registers[x] += 1
        return True

    def dec(self, x):
        if self.verbose:
            print("DEC", x)
        self.registers[x] -= 1
        return True

    def jnz(self, x, y):
        if self.verbose:
            print("JNZ", x, y)
        try:
            x = int(x)
        except ValueError:
            x = self.registers[x]

        if x != 0:
            self.current += int(y)
            try:
                cmd = self.instructions[self.current]
            except (TypeError, IndexError):
                return False
            return self._process_cmd(cmd)


class Project(object):
    def __init__(self, fh):
        self.input = fh

    def run1(self):
        machine = Machine(verbose=False)
        for line in self.input:
            machine.instructions.append(line.strip())

        while True:
            try:
                machine.process_current()
            except StopIteration:
                break

        return machine.registers['a']

    def run2(self):
        machine = Machine(verbose=False)
        machine.registers['c'] = 1

        for line in self.input:
            machine.instructions.append(line.strip())

        while True:
            try:
                machine.process_current()
            except StopIteration:
                break

        return machine.registers['a']


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        p = Project(f)
        print "Part 1:", p.run1()
        f.seek(0)
        print "Part 2:", p.run2()
