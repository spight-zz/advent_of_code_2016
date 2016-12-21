import re


class PachinkoDisc(object):
    def __init__(self, name, positions, current=0):
        self.num_positions = int(positions)
        self.current = int(current)
        self.name = name

    def open_in(self, turns):
        """Returns true if this disc will be open in `turns` turns"""
        return (self.current + turns) % self.num_positions == 0

    def tick(self):
        self.current = (self.current + 1) % self.num_positions

    def __str__(self):
        format_vars = dict(name=self.name,
                           pos=self.current,
                           max=self.num_positions)
        return "[{name}] at position {pos} of {max}".format(**format_vars)


class Pachinko(object):
    def __init__(self):
        self.discs = []
        self.time = 0

    def add_disc(self, disc):
        self.discs.append(disc)

    def tick(self):
        for disc in self.discs:
            disc.tick()
        self.time += 1

    def valid(self):
        for i, disc in enumerate(self.discs):
            if not disc.open_in(i + 1):
                return False
        return True

    def __str__(self):
        output = ""
        for disc in self.discs:
            output += str(disc) + "\n"
        return output


class Project(object):
    def __init__(self, fh):
        self.input = fh
        self.disc_pattern = re.compile(
                '(Disc #\d+) has (\d+) positions; '
                'at time=(\d+), it is at position (\d+).')

    def get_disc(self, line):
        match = self.disc_pattern.search(line)
        if match:
            disc = PachinkoDisc(match.group(1), match.group(2))
            at_zero = int(match.group(4)) - int(match.group(3))
            disc.current = at_zero
            return disc

    def run1(self, ):
        pachinko = Pachinko()
        for line in self.input:
            disc = self.get_disc(line.strip())
            pachinko.add_disc(disc)
        while not pachinko.valid():
            pachinko.tick()

        return pachinko.time

    def run2(self,):
        pachinko = Pachinko()
        for line in self.input:
            disc = self.get_disc(line.strip())
            pachinko.add_disc(disc)

        new_disc = PachinkoDisc("trollol", 11)
        pachinko.add_disc(new_disc)

        while not pachinko.valid():
            pachinko.tick()

        return pachinko.time


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        p = Project(f)
        print "Part 1:", p.run1()
        f.seek(0)
        print "Part 2:", p.run2()
