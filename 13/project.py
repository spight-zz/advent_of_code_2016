from queue import Queue


class Maze(object):
    def __init__(self, secret):
        self.secret = secret
        self.data = []

    def __str__(self):
        output = ""

        for j, col in enumerate(self.data):
            output += str(j) + " "
            for i, row in enumerate(col):
                if self.is_path(i, j):
                    output += ". "
                else:
                    output += "# "
            output += "\n"
        return output

    def expand_to(self, x, y):
        while len(self.data) < x + 1:
            self.data.append([])

        for row in self.data:
            while len(row) < y + 2:
                row.append(None)

    def get(self, x, y):
        self.expand_to(x, y)
        if self.data[x][y] is None:
            self.data[x][y] = self.is_path(x, y)
        return self.data[x][y]

    def is_path(self, x, y):
        hash_num = x*x + x*3 + 2*x*y + y + y*y + self.secret
        return bin(hash_num).count('1') % 2 == 0


class State(object):
    def __init__(self, maze, location, parent, distance,):
        self.maze = maze
        self.parent = parent
        self.distance = distance
        self.location = location

    def clone(self,):
        return State(self.maze, self.location, self.parent, self.distance)

    def move(self, x_y):
        new_locus = (self.location[0] + x_y[0], self.location[1] + x_y[1])
        self.location = new_locus

    def __str__(self):
        output = ""

        for j, col in enumerate(self.maze.data):
            output += "%03d " % j
            for i, row in enumerate(col):
                if (i, j) == self.location:
                    cur = True
                else:
                    cur = False
                if self.maze.is_path(i, j):
                    if cur:
                        output += "O "
                    else:
                        output += ". "
                else:
                    if cur:
                        output += "@ "
                    else:
                        output += "# "
            output += "\n"
        return output

    @property
    def itermoves(self):
        yield (0, 1)
        yield (0, -1)
        yield (1, 0)
        yield (-1, 0)

    @property
    def is_valid(self):
        if self.location[0] < 0 or self.location[1] < 0:
            return False
        return self.maze.get(*self.location)


def find_closest(maze, target=None, max_distance=None):
    queue = Queue()
    seen = {}

    root = State(maze, (1, 1), None, 0)
    queue.put(root)
    seen[root.location] = root
    maze.get(1, 1)

    while not queue.empty():
        state = queue.get()
        if max_distance and state.distance > max_distance:
            return seen

        if target is not None and state.location == target:
            print("超成功！！！！！")
            return state

        for move in state.itermoves:
            new_state = state.clone()
            new_state.parent = state
            new_state.distance += 1
            new_state.move(move)

            if new_state.is_valid and new_state.location not in seen:
                if max_distance is None or new_state.distance <= max_distance:
                    seen[new_state.location] = new_state
                    queue.put(new_state)

    return seen


def run1(code, target):
    maze = Maze(code)
    state = find_closest(maze, target=target)
    print(state.distance)


def run2(code, distance):
    maze = Maze(code)
    seen = find_closest(maze, max_distance=distance)
    print(len(seen.items()))


if __name__ == '__main__':
    run1(1362, (31, 39))
    run2(1362, 50)
