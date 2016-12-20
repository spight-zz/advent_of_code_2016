import sys
import re

class Project(object):
    def __init__(self, ):
        self.input = sys.stdin.read()
        self.compression_pattern = re.compile('(\((\d+)x(\d+)\))')

    def run1(self, ):
        self.output = ""
        self.pos = 0

        while True:
            try:
                self.find_next_decompression()
            except StopIteration:
                break

        print len(''.join(self.output.split()))

    def find_next_decompression(self):
        match = self.compression_pattern.search(self.input, self.pos)
        if match:
            # If there are uncompressed characters, add them to output here
            self.output += self.input[self.pos:match.start()]

            self.pos = match.start() + len(match.group(0))

            repeating = self.input[self.pos:self.pos + int(match.group(2))]
            self.output += repeating * int(match.group(3))

            self.pos += len(repeating)
        else:
            # Add remaining uncompressed characters
            self.output += self.input[self.pos:]
            raise StopIteration()

    def run2(self,):
        print self.calculate_expansion(self.input) - 1  # newline...

    def calculate_expansion(self, line):
        total = 0
        cur_pos = 0
        while cur_pos < len(line):
            match = self.compression_pattern.search(line, cur_pos)
            if match:
                total += match.start() - cur_pos  # No compression until matched location
                expand_pos = match.start() + len(match.group(1))
                expand_line = line[expand_pos:expand_pos + int(match.group(2))]
                total += self.calculate_expansion(expand_line) * int(match.group(3))
                cur_pos = expand_pos + int(match.group(2))
            else:
                total += len(line[cur_pos:])
                break
        return total


if __name__ == '__main__':
    p = Project()
    p.run1()
    p.run2()
