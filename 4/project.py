import sys

class Project(object):
    LETTERS = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
               'p','q','r','s','t','u','v','w','x','y','z']
    def __init__(self, ):
        pass

    def run1(self, ):
        total = 0
        for line in sys.stdin:
            parts = self.get_tuple(line)
            if self.checksum(parts[1]) == parts[2]:
                total += int(parts[0])
        print total

    def run2(self, ):
        for line in sys.stdin:
            parts = self.get_tuple(line)
            print(self.apply_cipher(parts), parts[0])


    def apply_cipher(self, parts):
        output = ''
        for c in parts[1]:
            if c == '-':
                output += ' '
                continue
            letter_id = self.LETTERS.index(c)
            letter_id = (letter_id + parts[0]) % 26
            output += self.LETTERS[letter_id]

        return output

    def get_tuple(self, line):
        data, checksum = line.strip().split('[')
        checksum = checksum[0:-1]
        parts = data.split('-')
        return int(parts[-1]), '-'.join(parts[0:-1]), checksum

    def checksum(self, data):
        last = None
        output = []
        for c in sorted(data):
            if c == '-':
                continue
            if c == last:
                output[-1][1] += 1
            else:
                output.append([c, 1])
                last = c

        most_common = sorted(output, key=lambda x: -x[1])[0:5]
        return ''.join(map(lambda x: x[0], most_common))






if __name__ == '__main__':
    Project().run2()
