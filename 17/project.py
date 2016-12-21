from Queue import Queue
from hashlib import md5


class Project(object):
    def __init__(self, fh):
        self.passcode = fh.read().strip()
        self.dir_map = [(0, 'U', (-1, 0)),
                        (1, 'D', (1, 0)),
                        (2, 'L', (0, -1)),
                        (3, 'R', (0, 1))]

    def iter_open_rooms(self, path_so_far):
        key = self.passcode + path_so_far
        hash_ = md5(key).hexdigest()

        cutoff = int('a', 16)
        for idx, char, move in self.dir_map:
            if int(hash_[idx], 16) > cutoff:
                yield char, move

    def is_valid(self, locus):
        return locus[0] in range(4) and locus[1] in range(4)

    def run1(self, ):
        target = (3, 3)
        queue = Queue()
        queue.put(("", (0, 0)))

        while not queue.empty():
            path_so_far, locus = queue.get()

            if locus == target:
                return path_so_far

            for char, move in self.iter_open_rooms(path_so_far):
                new_locus = (locus[0] + move[0], locus[1] + move[1])
                if self.is_valid(new_locus):
                    queue.put((path_so_far + char, new_locus))

    def run2(self, ):
        target = (3, 3)
        queue = Queue()
        queue.put(("", (0, 0)))
        longest = None

        while not queue.empty():
            path_so_far, locus = queue.get()

            if locus == target:
                longest = path_so_far
                continue

            for char, move in self.iter_open_rooms(path_so_far):
                new_locus = (locus[0] + move[0], locus[1] + move[1])
                if self.is_valid(new_locus):
                    queue.put((path_so_far + char, new_locus))

        return len(longest)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        p = Project(f)
        print "Part 1:", p.run1()
        f.seek(0)
        print "Part 2:", p.run2()
