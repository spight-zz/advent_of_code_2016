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
        print "%s receiving %s! (#%s)" % (self.name, value, len(self.items))

        if len(self.items) == 2:
            self.work()

    def work(self, ):
        print(self.items)
        if self.lower is None or self.higher is None:
            print("Output %s got too many items: %s" % (self.name, self.items))
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
            print line.strip()
            self.handle_line(line)

    def handle_line(self, line):
        matches = self.pattern.findall(line)
        if matches:
            self.build_objects(*matches)
            print(matches)
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
        if len(definitions) == 1:
            if definitions[0][0] == "value":
                return
            else:
                raise ValueError("Got a `bot` or `output` with too few instructions")
        for definition in definitions:
            if definition[0] == "bot":
                if self.workers.get(definition[1]) is None:
                    self.workers[definition[1]] = Worker("bot-" + definition[1])
            elif definition[0] == "output":
                if self.output.get(definition[1]) is None:
                    self.output[definition[1]] = Worker("output-" + definition[1])




if __name__ == '__main__':
    Project().run()
