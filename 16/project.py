import sys


class Project(object):
    def __init__(self, fh, disk_size):
        self.input = fh
        self.disk_size = disk_size
        self.inverse_map = {'0': '1', '1': '0'}
        self.check_map = {'00': '1', '11': '1', '01': '0', '10': '0'}

    def run(self, ):
        output = self.input.read().strip()
        while len(output) < self.disk_size:
            output = self.expand(output)
        output = output[0:self.disk_size]
        checksum = self.gen_checksum(output)
        return checksum

    def expand(self, data):
        return data + "0" + self.inversify(data)

    def inversify(self, line):
        line = reversed(line)
        return ''.join(map(lambda x: self.inverse_map[x], line))

    def gen_checksum(self, data):
        output = data
        while len(output) % 2 == 0:
            new_output = ""
            for pair in self.iterpairs(output):
                new_output += self.check_map[pair]
            output = new_output
        return output

    def iterpairs(self, data):
        pair = []
        for c in data:
            pair.append(c)
            if len(pair) == 2:
                yield str(pair[0]) + str(pair[1])
                pair = []


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        Project(f, 272)
        print "Part 1:", Project(f, 272).run()
        f.seek(0)
        print "Part 2:", Project(f, 35651584).run()
