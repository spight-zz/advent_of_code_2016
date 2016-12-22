import sys


class Project(object):
    def __init__(self, fh):
        self.input = fh

    def run1(self, ):
        num_elves = int(self.input.read())
        elves = range(num_elves)
        offset = 1
        while len(elves) > 1:
            next_offset = (len(elves) + offset) % 2
            elves = [elf for i, elf in enumerate(elves) if i % 2 != offset]

            offset = next_offset

        return elves[0] + 1

    def run2(self,):
        num_elves = int(self.input.read())
        elves = range(num_elves)
        i = 0
        while len(elves) > 1:
            target = (i + len(elves) / 2) % len(elves)
            del elves[target]
            if target > i:
                i += 1
            if i > len(elves) - 1:
                i = 0

        return elves[0] + 1


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        p = Project(f)
        print "Part 1:", p.run1()
        f.seek(0)
        print "Part 2:", p.run2()
