import sys


class Machine(object):
    def __init__(self, verbose=True):
        self.registers = dict(a=0, b=0, c=0, d=0)
        self.instructions = []
        self.current = 0
        self.output = []
        self.verbose = verbose

    def reset(self):
        self.registers = dict(a=0, b=0, c=0, d=0)
        self.current = 0
        self.output = []

    def process_current(self):
        try:
            cmd = self.instructions[self.current]
        except IndexError:
            return False
        # print cmd
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
        x = self.get_int(x)

        if y not in self.registers:
            print "Hyep'"
            return False

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
        # Note: You could probably turn this into a smart multiplication
        if self.verbose:
            print("JNZ", x, y)
        x = self.get_int(x)
        y = self.get_int(y)

        if x != 0:
            self.current += y
            try:
                cmd = self.instructions[self.current]
            except (TypeError, IndexError):
                return False
            return self._process_cmd(cmd)

    def tgl(self, reg):
        try:
            reg = self.registers[reg]
            editing = self.instructions[self.current + reg]
            parts = editing.split()
            changer = {
                'inc': 'dec',
                'dec': 'inc',
                'tgl': 'inc',
                'jnz': 'cpy',
                'cpy': 'jnz',
            }

            new_name = changer[parts[0]]
            new_instruction = ' '.join((new_name,) + tuple(parts[1:]))
            self.instructions[self.current + reg] = new_instruction
        except IndexError:
            return False

    def out(self, x):
        if self.verbose:
            print('OUT', x)
        x = self.get_int(x)
        self.output.append(x)

    def get_int(self, x):
        """Returns either a parsed int or the value of register at x"""
        try:
            return int(x)
        except ValueError:
            return self.registers[x]

    @property
    def state(self):
        return State(self.registers, self.current)


class State(object):
    def __init__(self, registers, current):
        self.registers = registers
        self.current = current

    @property
    def serialize(self):
        return str((str(self.registers), str(self.current)))


class Project(object):
    def __init__(self, fh):
        self.input = fh

    def valid_output(self, output):
        switch = 0
        for signal in output:
            if signal != switch:
                return False
            switch = (switch + 1) % 2

        return switch == 0


    def run1(self):
        machine = Machine(False)
        for line in self.input:
            machine.instructions.append(line.strip())

        i = 0
        while True:
            machine.reset()
            machine.registers['a'] = i
            seen = {}
            while machine.state.serialize not in seen:
                state = machine.state
                seen[state.serialize] = state

                machine.process_current()
                new_state = machine.state

            if self.valid_output(machine.output):
                return i
            i += 1

    def run2(self):
        return "Look up"


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        p = Project(f)
        print "Part 1:", p.run1()
        f.seek(0)
        print "Part 2:", p.run2()
