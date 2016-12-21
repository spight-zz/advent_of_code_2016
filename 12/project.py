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


    def lol(self, herp, derp):
        print(self)
        print(herp)
        print(derp)


class Project(object):
    def __init__(self, ):
        pass

    def run(self, ):
        machine = Machine(verbose=False)
        for line in sys.stdin:
            machine.instructions.append(line.strip())
        # print machine.process_current()
        # print machine.process_current()
        i = 0
        while i < 10000000000:
            i += 1
            if i % 1000 == 0:
                pass
                print("REGISTERS: %s" % machine.registers)
            try:
                machine.process_current()
            except StopIteration:
                break
        print machine.instructions
        print machine.registers




if __name__ == '__main__':
    Project().run()
