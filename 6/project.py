import sys
import operator


class Project(object):
    def __init__(self, fh):
        self.input = fh

    def run1(self, ):
        counts = [{}, {}, {}, {}, {}, {}, {}, {}]
        output = ""
        for line in self.input:
            for i, c in enumerate(line.strip()):
                if c in counts[i]:
                    counts[i][c] += 1
                else:
                    counts[i][c] = 1

        for count_dict in counts:
            output += self.most_common(count_dict)[0]

        return output

    def run2(self, ):
        counts = [{}, {}, {}, {}, {}, {}, {}, {}]
        output = ""
        for line in self.input:
            for i, c in enumerate(line.strip()):
                if c in counts[i]:
                    counts[i][c] += 1
                else:
                    counts[i][c] = 1

        for count_dict in counts:
            output += self.least_common(count_dict)[0]

        return output

    def to_idx(self, letter):
        return ord(letter.lower()) - 97

    def least_common(self, count_dict):
        return sorted(count_dict.items(), key=operator.itemgetter(1))[0]

    def most_common(self, count_dict):
        return sorted(count_dict.items(), key=operator.itemgetter(1))[-1]

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        p = Project(f)
        print "Part 1:", p.run1()
        f.seek(0)
        print "Part 2:", p.run2()
        f.close()
