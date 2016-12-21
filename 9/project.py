import sys
import re


class Project(object):
    def __init__(self, data):
        self.input = data
        self.compression_pattern = re.compile('(\((\d+)x(\d+)\))')

    def run1(self, ):
        self.output = ""
        self.pos = 0

        while True:
            try:
                self.find_next_decompression()
            except StopIteration:
                break

        return len(''.join(self.output.split()))

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
        return self.calculate_expansion(self.input) - 1  # -1 for newline. lol

    def calculate_expansion(self, line):
        total = 0
        cur_pos = 0
        while cur_pos < len(line):
            match = self.compression_pattern.search(line, cur_pos)
            if match:
                # No compression until we match a location
                total += match.start() - cur_pos
                expand_pos = match.start() + len(match.group(1))
                expand_line = line[expand_pos:expand_pos + int(match.group(2))]
                expanded_size = self.calculate_expansion(expand_line)
                total += expanded_size * int(match.group(3))
                cur_pos = expand_pos + int(match.group(2))
            else:
                total += len(line[cur_pos:])
                break
        return total


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        p = Project(f.read())
        print "Part 1:", p.run1()
        print "Part 2:", p.run2()
