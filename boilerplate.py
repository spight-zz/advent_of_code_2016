import sys


class Project(object):
    def __init__(self, fh):
        self.input = fh

    def run1(self, ):
        for line in self.input:
            pass

    def run2(self,):
        for line in self.input:
            pass


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        p = Project(f)
        print "Part 1:", p.run1()
        f.seek(0)
        print "Part 2:", p.run2()
