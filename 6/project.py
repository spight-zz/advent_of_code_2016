import sys
import operator

class Project(object):
    def __init__(self, ):
        pass

    def run1(self, ):
        counts = [{}, {}, {}, {}, {}, {}, {}, {}]
        output = ""
        for line in sys.stdin:
            for i, c in enumerate(line.strip()):
                if c in counts[i]:
                    counts[i][c] += 1
                else:
                    counts[i][c] = 1

        for count_dict in counts:
            output += self.most_common(count_dict)[0]

        print output

    def run2(self, ):
        counts = [{}, {}, {}, {}, {}, {}, {}, {}]
        output = ""
        for line in sys.stdin:
            for i, c in enumerate(line.strip()):
                if c in counts[i]:
                    counts[i][c] += 1
                else:
                    counts[i][c] = 1

        for count_dict in counts:
            output += self.least_common(count_dict)[0]

        print output


    def to_idx(self, letter):
        return ord(letter.lower()) - 97

    def least_common(self, count_dict):
        return sorted(count_dict.items(), key=operator.itemgetter(1))[0]

    def most_common(self, count_dict):
        return sorted(count_dict.items(), key=operator.itemgetter(1))[-1]

if __name__ == '__main__':
    # Project().run1()
    Project().run2()
