""" Note, sort the input.txt file numerically before running
sort -n input.txt > tmp.txt && mv -f tmp.txt input.txt
"""
import sys


class Project(object):
    def __init__(self, fh):
        self.input = fh

    def int_to_ip(self, data):
        binary = bin(data)[2:].zfill(32)

        sects = []
        while len(binary) > 0:
            sects.append(str(int(binary[0:8], 2)))

            binary = binary[8:]
        return '.'.join(sects)

    def run1(self, ):
        greatest = 0
        for line in self.input:
            parts = line.strip().split('-')
            low = int(parts[0])
            high = int(parts[1])

            if low > greatest + 1:
                return greatest + 1
                self.int_to_ip(greatest + 1)
            if high > greatest:
                greatest = high

    def run2(self, ):
        greatest = 0
        valid = 0
        for line in self.input:
            parts = line.strip().split('-')
            low = int(parts[0])
            high = int(parts[1])

            if low > greatest + 1:
                valid += low - greatest - 1

            if high > greatest:
                greatest = high
        return valid


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        p = Project(f)
        print "Part 1:", p.run1()
        f.seek(0)
        print "Part 2:", p.run2()
