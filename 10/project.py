import sys
import re


OUTPUT = {}


class Worker(object):
    def __init__(self, name, lower=None, higher=None):
        self.name = name
        self.lower = lower
        self.higher = higher
        self.items = []

    def give(self, value):
        self.items.append(value)

        if len(self.items) == 2:
            self.work()

    def work(self, ):
        if self.items[0] in (61, 17) and self.items[1] in (61, 17):
            print("Worker %s handling values 67 and 17" % self.name)

        if self.items[0] > self.items[1]:
            self.lower.give(self.items[0])
            self.higher.give(self.items[1])
        else:
            self.lower.give(self.items[1])
            self.higher.give(self.items[0])

        self.items = []


class Project(object):
    def __init__(self, ):
        self.workers = {}
        self.output = {}
        self.pattern = re.compile('(bot|value|output) (\d+)')

    def run(self, ):
        for line in sys.stdin:
            self.handle_line(line)

        total = 1
        for name in ['0', '1', '2']:
            total *= self.output[name].items[0]
        print total

    def handle_line(self, line):
        matches = self.pattern.findall(line)
        if matches:
            self.build_objects(*matches)
            if matches[0][0] == "value":
                self.workers[matches[1][1]].give(int(matches[0][1]))
            elif matches[0][0] == "bot":
                self.plumb(self.workers[matches[0][1]], matches[1], matches[2])

    def plumb(self, worker, higher, lower):
        """ Connect the worker to higher and lower.
            worker is a Worker instance
            higher and lower are tuples of strings describing workers or output
        """
        higher_target = None
        lower_target = None
        if higher[0] == "bot":
            higher_target = self.workers[higher[1]]
        else:
            higher_target = self.output[higher[1]]

        if lower[0] == "bot":
            lower_target = self.workers[lower[1]]
        else:
            lower_target = self.output[lower[1]]

        worker.lower = lower_target
        worker.higher = higher_target

    def build_objects(self, *definitions):
        """definitions is list of tuples of type (bot/output) and number"""
        if len(definitions) == 1:  # Value object. Don't need to build
            return
        for parts in definitions:
            if parts[0] == "bot":
                if self.workers.get(parts[1]) is None:
                    self.workers[parts[1]] = Worker("bot-" + parts[1])

            elif parts[0] == "output":
                if self.output.get(parts[1]) is None:
                    self.output[parts[1]] = Worker("output-" + parts[1])


if __name__ == '__main__':
    Project().run()
