import hashlib


class Project(object):
    def __init__(self, unique_id):
        self.id = unique_id

    def run1(self, ):
        output = ""
        i = 0
        for found, _ in self.next:
            i += 1
            output += found
            if i == 8:
                break
        return output

    def run2(self, ):
        output = [None] * 8
        i = 0
        for pos, found in self.next:
            try:
                pos = int(pos)
            except ValueError:
                continue
            if pos < 8 and output[pos] is None:
                output[pos] = found
                i += 1
                if i == 8:
                    break

        return ''.join(output)

    @property
    def next(self):
        i = 0
        while True:
            key = self.id + str(i)
            hashed = hashlib.md5(key).hexdigest()
            if hashed.startswith('00000'):
                yield hashed[5], hashed[6]
            i += 1


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        p = Project(f.read().strip())
        print "Part 1:", p.run1()
        print "Part 2:", p.run2()
