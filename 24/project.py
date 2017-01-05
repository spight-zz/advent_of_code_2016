import sys
from Queue import Queue
from itertools import combinations, permutations


class Maze(object):
    def __init__(self, matrix):
        self.maze = []
        self.goals = {}
        self.init_maze(matrix)

    def __str__(self):
        output = ""
        rev_lookup = {}
        for key, value in self.goals.iteritems():
            rev_lookup[value] = key

        for i, row in enumerate(self.maze):
            for j, point in enumerate(row):
                if not point:
                    output += "#"
                elif (i, j) not in rev_lookup:
                    output += "."
                else:
                    output += str(rev_lookup[(i, j)])
            output += "\n"

        return output

    def init_maze(self, matrix):
        """Sets self.maze to a two-dimensional array"""
        for line in matrix:
            self.add_row()
            for char in line.strip():
                if char == '#':
                    self.maze[-1].append(False)
                else:
                    try:
                        goal_num = int(char)
                        locus = (len(self.maze) - 1, len(self.maze[-1]))
                        self.goals[goal_num] = locus

                    except ValueError:
                        pass
                    finally:
                        self.maze[-1].append(True)

    def add_row(self):
        self.maze.append([])

    def iter_moves(self, locus):
        if locus[0] > 0 and self.maze[locus[0] - 1][locus[1]]:
            yield (-1, 0)

        if locus[0] < len(self.maze) - 1 and self.maze[locus[0] + 1][locus[1]]:
            yield (1, 0)

        row = self.maze[locus[0]]
        if locus[1] > 0 and row[locus[1] - 1]:
            yield (0, -1)

        if locus[1] < len(row) - 1 and row[locus[1] + 1]:
            yield (0, 1)

    def find_distance_between(self, begin, end):
        seen = {}
        queue = Queue()
        root = State(begin, None, 0)
        queue.put(root)

        while not queue.empty():
            state = queue.get()

            if state.locus == end:
                return state.distance

            for move in self.iter_moves(state.locus):
                new_state = state.move(move)
                if new_state.serialize not in seen:
                    seen[new_state.serialize] = new_state
                    queue.put(new_state)


class State(object):
    def __init__(self, locus, parent, distance):
        self.locus = locus
        self.parent = parent
        self.distance = distance

    def move(self, move):
        """Creates a new state with distance + 1 and moved locus"""
        new_locus = (self.locus[0] + move[0], self.locus[1] + move[1])
        return State(new_locus, self, self.distance + 1)

    @property
    def serialize(self):
        return str(self.locus)


class Node(object):
    def __init__(self, data):
        self.data = data
        self.nodes = {}

    def __repr__(self):
        return "<Node: %s>" % str(self.data)

    def add_node(self, new_node, distance):
        if new_node in self.nodes:
            return True
        else:
            self.nodes[new_node] = distance
            new_node.add_node(self, distance)


class Project(object):
    def __init__(self, fh):
        self.input = fh

    def run1(self, ):
        maze = Maze(self.input)
        nodes = [Node(n) for n in range(8)]
        for combo in combinations(nodes, 2):
            distance = maze.find_distance_between(maze.goals[combo[0].data],
                                                  maze.goals[combo[1].data])
            combo[0].add_node(combo[1], distance)

        minimum = None

        for perm in permutations(range(1, 8), 7):
            distance = 0
            last = 0  # start at node 0
            for idx in perm:
                distance += nodes[last].nodes[nodes[idx]]
                last = idx

            if minimum is None or distance < minimum[0]:
                minimum = (distance, perm)
        return minimum

    def run2(self,):
        maze = Maze(self.input)
        nodes = [Node(n) for n in range(8)]
        for combo in combinations(nodes, 2):
            distance = maze.find_distance_between(maze.goals[combo[0].data],
                                                  maze.goals[combo[1].data])
            combo[0].add_node(combo[1], distance)

        minimum = None

        for perm in permutations(range(1, 8), 7):
            distance = 0
            last = 0  # start at node 0
            for idx in perm:
                distance += nodes[last].nodes[nodes[idx]]
                last = idx
            distance += nodes[last].nodes[nodes[0]]

            if minimum is None or distance < minimum[0]:
                minimum = (distance, perm)
        return minimum


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        p = Project(f)
        print "Part 1:", p.run1()
        f.seek(0)
        print "Part 2:", p.run2()
